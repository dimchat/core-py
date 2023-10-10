# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from typing import Optional, Any, Dict

from mkm.format import utf8_encode
from mkm.format import TransportableData

from dkd import SecureMessage

from .base import BaseMessage


"""
    Secure Message
    ~~~~~~~~~~~~~~
    Instant Message encrypted by a symmetric key

    data format: {
        //-- envelope
        sender   : "moki@xxx",
        receiver : "hulk@yyy",
        time     : 123,
        //-- content data and key/keys
        data     : "...",  // base64_encode( symmetric_encrypt(content))
        key      : "...",  // base64_encode(asymmetric_encrypt(password))
        keys     : {
            "ID1": "key1", // base64_encode(asymmetric_encrypt(password))
        }
    }
"""


class EncryptedMessage(BaseMessage, SecureMessage):

    def __init__(self, msg: Dict[str, Any]):
        super().__init__(msg=msg)
        # lazy
        self.__data: Optional[bytes] = None
        self.__key: Optional[TransportableData] = None
        self.__keys: Optional[Dict] = None

    @property  # Override
    def data(self) -> bytes:
        if self.__data is None:
            text = self.get('data')
            if text is None:
                assert False, 'message data cannot be empty: %s' % self
            elif not BaseMessage.is_broadcast(msg=self):
                # message content had been encrypted by a symmetric key,
                # so the data should be encoded here (with algorithm 'base64' as default).
                self.__data = TransportableData.decode(text)
            elif isinstance(text, str):
                # broadcast message content will not be encrypted (just encoded to JsON),
                # so return the string data directly
                self.__data = utf8_encode(string=text)  # JsON
            else:
                assert False, 'content data error: %s' % text
        return self.__data

    @property  # Override
    def encrypted_key(self) -> Optional[bytes]:
        ted = self.__key
        if ted is None:
            base64 = self.get('key')
            if base64 is None:
                # check 'keys'
                keys = self.encrypted_keys
                if keys is not None:
                    receiver = str(self.receiver)
                    base64 = keys.get(receiver)
            self.__key = ted = TransportableData.parse(base64)
        # decode data
        if ted is not None:
            return ted.data

    @property  # Override
    def encrypted_keys(self) -> Optional[Dict[str, Any]]:
        if self.__keys is None:
            self.__keys = self.get('keys')
        return self.__keys
