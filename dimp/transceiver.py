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

from mkm import SymmetricKey

from dkd import Content, ContentType, ForwardContent
from dkd import InstantMessage, SecureMessage, ReliableMessage

from .protocol import FileContent, Protocol
from .delegate import ICallback, ICompletionHandler, ITransceiverDelegate


class Transceiver(Protocol):

    def __init__(self):
        super().__init__()

        # delegates
        self.delegate: ITransceiverDelegate = None

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
                # sending group message one by one
                for r_msg in messages:
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
        if msg.delegate is None:
            msg.delegate = self
        if group is None:
            # personal message
            password = self.load_password(sender=sender, receiver=receiver)
            s_msg = msg.encrypt(password=password)
        else:
            # group message
            password = self.load_password(sender=sender, receiver=group.identifier)
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
            # do it again to drop the wrapper,
            # the secret inside the content is the real message
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
        # encrypt content
        return super().encrypt_content(content=content, key=password, msg=msg)

    def decrypt_content(self, data: bytes, key: dict, msg: SecureMessage) -> Content:
        password = SymmetricKey(key=key)
        if password is not None:
            # decrypt content
            content = super().decrypt_content(data=data, key=password, msg=msg)
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
