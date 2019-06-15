# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

"""
    Transceiver
    ~~~~~~~~~~~

    Delegate to process message transforming
"""

import json
from abc import ABCMeta, abstractmethod

from mkm import SymmetricKey
from mkm import Meta, ID
from mkm import IUserDataSource, IGroupDataSource

from dkd import Content, InstantMessage, SecureMessage, ReliableMessage
from dkd import IInstantMessageDelegate, ISecureMessageDelegate, IReliableMessageDelegate

from .protocol import MessageType, ForwardContent
from .barrack import IBarrackDelegate


class ICallback(metaclass=ABCMeta):

    def finished(self, result, error):
        pass


class ICompletionHandler(metaclass=ABCMeta):

    def success(self):
        pass

    def failed(self, error):
        pass


class Transceiver(IInstantMessageDelegate, ISecureMessageDelegate, IReliableMessageDelegate):

    def __init__(self):
        super().__init__()

        # delegates
        self.delegate: ITransceiverDelegate = None
        self.dataSource: ITransceiverDataSource = None

        self.userDataSource: IUserDataSource = None
        self.groupDataSource: IGroupDataSource = None

    def send_message(self, msg: InstantMessage, callback: ICallback, split: bool) -> bool:
        """
        Send message (secured + certified) to target station

        :param msg:      instant message
        :param callback: callback function
        :param split:    if it's a group message, split it before sending out
        :return:         False on data/delegate error
        """
        r_msg = self.encrypt_sign(msg=msg)
        if r_msg is None:
            raise AssertionError('failed to encrypt and sign message: %s' % msg)
        # trying to send out
        receiver = ID(msg.envelope.receiver)
        group = ID(msg.content.group)
        ok = True
        if split and receiver.type.is_group():
            members = self.groupDataSource.members(identifier=group)
            messages = r_msg.split(members=members)
            for r_msg in messages:
                # sending group message one by one
                if not self.__send_message(msg=r_msg, callback=callback):
                    ok = False
        else:
            ok = self.__send_message(msg=r_msg, callback=callback)
        # TODO: set iMsg.state = sending/waiting
        return ok

    def __send_message(self, msg: ReliableMessage, callback: ICallback) -> bool:

        class CompletionHandler(ICompletionHandler):

            def __init__(self, m: ReliableMessage, cb: ICallback):
                super().__init__()
                self.msg = m
                self.callback = cb

            def success(self):
                self.callback.finished(result=self.msg, error=None)

            def failed(self, error):
                self.callback.finished(result=self.msg, error=error)

        data = json.dumps(msg).encode('utf-8')
        handler = CompletionHandler(m=msg, cb=callback)
        return self.delegate.send_package(data=data, handler=handler)

    #
    #   Conveniences
    #
    def encrypt_sign(self, msg: InstantMessage) -> ReliableMessage:
        """
        Pack instant message to reliable message for delivering

        :param msg: instant message
        :return:    ReliableMessage object
        """
        if msg.delegate is None:
            msg.delegate = self
        sender = ID(msg.envelope.sender)
        receiver = ID(msg.envelope.receiver)
        group = ID(msg.content.group)
        # if 'group' exists and the 'receiver' is a group ID,
        # they must be equal
        if group is None and receiver.type.is_group():
            group = receiver
        # 1. encrypt 'content' to 'data' for receiver
        if group is not None:
            # group message
            members = []
            if receiver.type.is_communicator():
                # split group message
                members.append(receiver)
            else:
                members = self.groupDataSource.members(identifier=group)
            password = self.__password(sender=sender, receiver=group)
            s_msg = msg.encrypt(password=password, members=members)
        else:
            # personal message
            password = self.__password(sender=sender, receiver=receiver)
            s_msg = msg.encrypt(password=password)
        # 2. sign 'data' by sender
        s_msg.delegate = self
        return s_msg.sign()

    def __password(self, sender: ID, receiver: ID) -> SymmetricKey:
        # 1. get old key from store
        reused_key = self.dataSource.cipher_key(sender=sender, receiver=receiver)
        # 2. get new key from delegate
        new_key = self.dataSource.reuse_cipher_key(sender=sender, receiver=receiver, key=reused_key)
        if new_key is None:
            new_key = reused_key
        if new_key is None:
            # 3. create a new key
            new_key = SymmetricKey(key={'algorithm': 'AES'})
        # 4. save it into the key store
        if new_key != reused_key:
            self.dataSource.cache_cipher_key(key=new_key, sender=sender, receiver=receiver)
        return new_key

    def verify_decrypt(self, msg: ReliableMessage) -> InstantMessage:
        sender = ID(msg.envelope.sender)
        receiver = ID(msg.envelope.receiver)
        # [Meta Protocol] check meta in first contact message
        meta = self.userDataSource.meta(identifier=sender)
        if meta is None:
            # first contact, try meta in message package
            meta = msg.meta
            if meta is None:
                # TODO: query meta for sender from DIM network
                raise LookupError('failed to get meta for sender: %s' % sender)
            meta = Meta(meta)
            if meta.match_identifier(identifier=sender):
                self.dataSource.save_meta(meta=meta, identifier=sender)
            else:
                raise ValueError('meta not match %s, %s' % (sender, meta))
        # 1. verify 'data' with 'signature'
        if msg.delegate is None:
            msg.delegate = self
        s_msg = msg.verify()

        # 2. decrypt 'data' to 'content'
        user = self.delegate.user(identifier=receiver)
        if user is None:
            raise AssertionError('wrong recipient: %s' % receiver)
        group = ID(msg.group)
        if group is not None:
            # trim for user(group member)
            s_msg = s_msg.trim(member=receiver)
            s_msg.delegate = self
            i_msg = s_msg.decrypt(member=receiver)
        else:
            # personal message
            s_msg.delegate = self
            i_msg = s_msg.decrypt()
        # 3. check: top-secret message
        if i_msg.content.type == MessageType.Forward:
            content = ForwardContent(i_msg.content)
            return self.verify_decrypt(content.forward)
        # OK
        return i_msg

    #
    #   IInstantMessageDelegate
    #
    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        # TODO: check attachment for File/Image/Audio/Video message content before
        password = SymmetricKey(key)
        if password is not None:
            string = json.dumps(content)
            return password.encrypt(data=string.encode('utf-8'))

    def encrypt_key(self, key: dict, receiver: str, msg: InstantMessage) -> bytes:
        contact = self.delegate.account(identifier=ID(receiver))
        if contact is not None:
            string = json.dumps(key)
            return contact.encrypt(data=string.encode('utf-8'))

    #
    #   ISecureMessageDelegate
    #
    def decrypt_key(self, key: bytes, sender: str, receiver: str, msg: SecureMessage) -> dict:
        sender = ID(sender)
        receiver = ID(receiver)
        if key is not None:
            # decrypt key data with the receiver's private key
            identifier = ID(msg.envelope.receiver)
            user = self.delegate.user(identifier=identifier)
            data = user.decrypt(data=key)
            if data is None:
                raise AssertionError('failed to decrypt key data')
            # create symmetric key from JsON data
            key = SymmetricKey(json.loads(data.decode('utf-8')))
            if key is not None:
                self.dataSource.cache_cipher_key(key=key, sender=sender, receiver=receiver)
        if key is None:
            # if key data is empty, get it from key store
            key = self.dataSource.cipher_key(sender=sender, receiver=receiver)
        return key

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Content:
        password = SymmetricKey(key)
        if password is not None:
            plaintext = password.decrypt(data)
            if plaintext is not None:
                # TODO: check attachment for File/Image/Audio/Video message content after
                return Content(json.loads(plaintext))

    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        user = self.delegate.user(identifier=ID(sender))
        if user is not None:
            return user.sign(data)

    #
    #   IReliableMessageDelegate
    #
    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        contact = self.delegate.account(identifier=ID(sender))
        if contact is not None:
            return contact.verify(data=data, signature=signature)


#
#  Delegates
#
class ITransceiverDataSource(metaclass=ABCMeta):

    @abstractmethod
    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        """
        Save meta for entity ID

        :param meta:       meta info
        :param identifier: entity ID
        :return:           False on meta not match with the entity ID
        """
        pass

    @abstractmethod
    def cipher_key(self, sender: ID, receiver: ID) -> SymmetricKey:
        """
        Get cipher key for encrypt message from 'sender' to 'receiver'

        :param sender:   user ID
        :param receiver: contact/group ID
        :return:         cipher key
        """
        pass

    @abstractmethod
    def cache_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID) -> bool:
        """
        Cache cipher key for reusing, with direction ('sender' to 'receiver')

        :param key:      cipher key from a contact
        :param sender:   contact ID
        :param receiver: user/group ID
        :return:         cipher key
        """
        pass

    @abstractmethod
    def reuse_cipher_key(self, sender: ID, receiver: ID, key: SymmetricKey) -> SymmetricKey:
        """
        Update/create cipher key for encrypt message content

        :param sender:   user ID
        :param receiver: contact/group ID
        :param key:      old key to be reused (nullable)
        :return:         new key
        """
        pass


class ITransceiverDelegate(IBarrackDelegate, metaclass=ABCMeta):

    @abstractmethod
    def send_package(self, data: bytes, handler: ICompletionHandler) -> bool:
        """
        Send out a data package onto network

        :param data:    package data
        :param handler: completion handler
        :return:        False on data/delegate error
        """
        pass

    # def upload_file_data(self, data: bytes, msg: InstantMessage) -> str:
    #     """
    #     Upload encrypted data to CDN
    #
    #     :param data: encrypted file data
    #     :param msg:  instant message
    #     :return:     download URL
    #     """
    #     pass
    #
    # def download_file_data(self, url: str, msg: InstantMessage) -> bytes:
    #     """
    #     Download encrypted data from CDN, and decrypt it when finished
    #
    #     :param url: download URL
    #     :param msg: instant message
    #     :return:    encrypted file data
    #     """
    #     pass
