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
from typing import Optional

from mkm import SymmetricKey, Meta, ID, is_broadcast
from mkm.crypto.utils import base64_encode, base64_decode

from dkd import Content, InstantMessage, SecureMessage, ReliableMessage, Message
from dkd import IInstantMessageDelegate, IReliableMessageDelegate

from .protocol import ContentType, ForwardContent, FileContent
from .delegate import ICallback, ICompletionHandler, ITransceiverDelegate
from .delegate import ISocialNetworkDataSource, ICipherKeyDataSource


class Transceiver(IInstantMessageDelegate, IReliableMessageDelegate):

    def __init__(self):
        super().__init__()

        # delegates
        self.delegate: ITransceiverDelegate = None
        self.barrack: ISocialNetworkDataSource = None
        self.key_cache: ICipherKeyDataSource = None

    def __load_password(self, sender: ID, receiver: ID) -> SymmetricKey:
        # 1. get old key from store
        old_key = self.key_cache.cipher_key(sender=sender, receiver=receiver)
        # 2. get new key from delegate
        new_key = self.key_cache.reuse_cipher_key(key=old_key, sender=sender, receiver=receiver)
        if new_key is None:
            if old_key is None:
                # 3. create a new key
                new_key = SymmetricKey(key={'algorithm': 'AES'})
            else:
                new_key = old_key
        # 4. update new key into the key store
        if new_key != old_key:
            self.key_cache.cache_cipher_key(key=new_key, sender=sender, receiver=receiver)
        return new_key

    def __save_password(self, password: dict, sender: ID, receiver: ID) -> SymmetricKey:
        key = SymmetricKey(password)
        if key is not None:
            # cache the new key in key store
            self.key_cache.cache_cipher_key(key=key, sender=sender, receiver=receiver)
        return key

    def is_broadcast_message(self, msg: Message) -> bool:
        receiver = self.barrack.identifier(msg.group)
        if receiver is None:
            receiver = self.barrack.identifier(msg.envelope.receiver)
        return is_broadcast(receiver)

    #
    #   Send message
    #
    def send_message(self, msg: InstantMessage, callback: ICallback, split: bool) -> bool:
        """
        Send message (secured + certified) to target station

        :param msg:      instant message
        :param callback: callback function
        :param split:    if it's a group message, split it before sending out
        :return:         False on data/delegate error
        """
        # transforming
        r_msg = self.encrypt_sign(msg=msg)
        if r_msg is None:
            raise AssertionError('failed to encrypt and sign message: %s' % msg)
        # trying to send out
        ok = True
        receiver = self.barrack.identifier(msg.envelope.receiver)
        if split and receiver.type.is_group():
            group = self.barrack.group(identifier=receiver)
            if group is None:
                raise LookupError('failed to create group: %s' % receiver)
            messages = r_msg.split(members=group.members)
            if messages is None:
                # failed to split msg, send it to group
                ok = self.__send_message(msg=r_msg, callback=callback)
            else:
                for r_msg in messages:
                    # sending group message one by one
                    if not self.__send_message(msg=r_msg, callback=callback):
                        ok = False
        else:
            ok = self.__send_message(msg=r_msg, callback=callback)
        # TODO: if OK, set iMsg.state = sending; else set iMsg.state = waiting
        return ok

    class CompletionHandler(ICompletionHandler):

        def __init__(self, msg: ReliableMessage, cb: ICallback):
            super().__init__()
            self.msg = msg
            self.callback = cb

        def success(self):
            self.callback.finished(result=self.msg, error=None)

        def failed(self, error):
            self.callback.finished(result=self.msg, error=error)

    def __send_message(self, msg: ReliableMessage, callback: ICallback) -> bool:
        data = json.dumps(msg).encode('utf-8')
        handler = Transceiver.CompletionHandler(msg=msg, cb=callback)
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
        sender = self.barrack.identifier(msg.envelope.sender)
        receiver = self.barrack.identifier(msg.envelope.receiver)
        # if 'group' exists and the 'receiver' is a group ID,
        # they must be equal
        group = None
        if receiver.type.is_group():
            group = self.barrack.group(identifier=receiver)
        else:
            gid = msg.group
            if gid is not None:
                gid = self.barrack.identifier(gid)
                group = self.barrack.group(identifier=gid)
        # 1. encrypt 'content' to 'data' for receiver
        if group is None:
            # personal message
            password = self.__load_password(sender=sender, receiver=receiver)
            s_msg = msg.encrypt(password=password)
        else:
            # group message
            password = self.__load_password(sender=sender, receiver=group.identifier)
            s_msg = msg.encrypt(password=password, members=group.members)
        # 2. sign 'data' by sender
        s_msg.delegate = self
        return s_msg.sign()

    def verify_decrypt(self, msg: ReliableMessage) -> InstantMessage:
        """
        Extract instant message from a reliable message received

        :param msg:
        :return:
        """
        sender = self.barrack.identifier(msg.envelope.sender)
        # [Meta Protocol] check meta in first contact message
        meta = self.barrack.meta(identifier=sender)
        if meta is None:
            # first contact, try meta in message package
            meta = Meta(msg.meta)
            if meta is None:
                # TODO: query meta for sender from DIM network
                raise LookupError('failed to get meta for sender: %s' % sender)
            assert meta.match_identifier(identifier=sender), 'meta not match: %s, %s' % (sender, meta)
            if not self.barrack.save_meta(meta=meta, identifier=sender):
                raise ValueError('save meta error: %s, %s' % (sender, meta))

        # 1. verify 'data' with 'signature'
        if msg.delegate is None:
            msg.delegate = self
        s_msg = msg.verify()

        # 2. decrypt 'data' to 'content'
        if s_msg.delegate is None:
            s_msg.delegate = self
        i_msg = s_msg.decrypt()

        # 3. check: top-secret message
        if i_msg.content.type == ContentType.Forward:
            content: ForwardContent = i_msg.content
            r_msg = content.forward
            secret = self.verify_decrypt(msg=r_msg)
            if secret is not None:
                return secret
            # FIXME: not for you?
        # OK
        return i_msg

    #
    #   IInstantMessageDelegate
    #
    def encrypt_content(self, content: Content, key: dict, msg: InstantMessage) -> bytes:
        password = SymmetricKey(key)
        if password is None:
            raise AssertionError('failed to get symmetric key: %s' % key)
        # check attachment for File/Image/Audio/Video message content before
        if isinstance(content, FileContent):
            data = password.encrypt(data=content.data)
            # upload (encrypted) file data onto CDN and save the URL in message content
            url = self.delegate.upload_data(data=data, msg=msg)
            if url is not None:
                content.url = url
                content.data = None
        # encrypt with password
        string = json.dumps(content)
        return password.encrypt(data=string.encode('utf-8'))

    def encode_content_data(self, data: bytes, msg: InstantMessage) -> str:
        if self.is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so no need to encode to Base64 here
            return data.decode('utf-8')
        # encode to Base64
        return base64_encode(data)

    def encrypt_key(self, key: dict, receiver: str, msg: InstantMessage) -> Optional[bytes]:
        if self.is_broadcast_message(msg=msg):
            # broadcast message has no key
            return None
        # TODO: check whether support reused key

        # encrypt with receiver's public key
        contact = self.barrack.account(identifier=self.barrack.identifier(receiver))
        if contact is not None:
            string = json.dumps(key)
            return contact.encrypt(data=string.encode('utf-8'))

    def encode_key_data(self, key: bytes, msg: InstantMessage) -> Optional[str]:
        assert not self.is_broadcast_message(msg=msg) or key is None, 'broadcast message has no key'
        # encode to Base64
        if key is not None:
            return base64_encode(key)

    #
    #   ISecureMessageDelegate
    #
    def decrypt_key(self, key: bytes, sender: str, receiver: str, msg: SecureMessage) -> Optional[dict]:
        assert not self.is_broadcast_message(msg=msg) or key is None, 'broadcast message has no key'
        sender = self.barrack.identifier(sender)
        receiver = self.barrack.identifier(receiver)
        password = None
        if key is not None:
            # decrypt key data with the receiver's private key
            identifier = self.barrack.identifier(msg.envelope.receiver)
            user = self.barrack.user(identifier=identifier)
            data = user.decrypt(data=key)
            if data is None:
                raise AssertionError('failed to decrypt key data')
            # create symmetric key from JsON data
            pw = json.loads(data.decode('utf-8'))
            password = self.__save_password(password=pw, sender=sender, receiver=receiver)
        if password is None:
            # if key data is empty, get it from key store
            password = self.key_cache.cipher_key(sender=sender, receiver=receiver)
        return password

    def decode_key_data(self, key: str, msg: SecureMessage) -> Optional[bytes]:
        assert not self.is_broadcast_message(msg=msg) or key is None, 'broadcast message has no key'
        # decode from Base64
        if key is not None:
            return base64_decode(key)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Content:
        password = SymmetricKey(key=key)
        if password is not None:
            plaintext = password.decrypt(data)
            if plaintext is not None:
                content = Content(json.loads(plaintext))
                # check attachment for File/Image/Audio/Video message content after
                if isinstance(content, FileContent):
                    i_msg = InstantMessage.new(content=content, envelope=msg.envelope)
                    # download from CDN
                    file_data = self.delegate.download_data(content.url, i_msg)
                    if file_data is None:
                        # save symmetric key for decrypted file data after download from CDN
                        content.password = password
                    else:
                        # decrypt file data
                        content.data = password.decrypt(data=file_data)
                        assert content.data is not None, 'failed to decrypt file data with key: %s' % key
                        content.url = None
                return content

    def decode_content_data(self, data: str, msg: SecureMessage) -> bytes:
        if self.is_broadcast_message(msg=msg):
            # broadcast message content will not be encrypted (just encoded to JsON),
            # so return the string data directly
            return data.encode('utf-8')
        # decode from Base64
        return base64_decode(data)

    def sign_data(self, data: bytes, sender: str, msg: SecureMessage) -> bytes:
        user = self.barrack.user(identifier=self.barrack.identifier(sender))
        if user is not None:
            return user.sign(data)

    def encode_signature(self, signature: bytes, msg: SecureMessage) -> str:
        return base64_encode(signature)

    #
    #   IReliableMessageDelegate
    #
    def verify_data_signature(self, data: bytes, signature: bytes, sender: str, msg: ReliableMessage) -> bool:
        contact = self.barrack.account(identifier=self.barrack.identifier(sender))
        if contact is not None:
            return contact.verify(data=data, signature=signature)

    def decode_signature(self, signature: str, msg: ReliableMessage) -> bytes:
        return base64_decode(signature)
