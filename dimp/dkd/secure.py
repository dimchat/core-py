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

from typing import Optional, Dict

from mkm.format import TransportableData
from dkd.protocol import SecureMessage

from ..format import PlainData

from .base import BaseMessage


"""
    Secure Message
    ~~~~~~~~~~~~~~
    Instant Message encrypted by a symmetric key

    data format: {
        //-- envelope
        "sender"   : "moki@xxx",
        "receiver" : "hulk@yyy",
        "time"     : 123.45,
        
        //-- content data and key/keys
        "data"     : "...",    // base64_encode( symmetric_encrypt(content))
        "keys"     : {
            "ID1"    : "key1", // base64_encode(asymmetric_encrypt(password))
            "digest" : "..."   // hash(pwd.data)
        }
    }
"""


class EncryptedMessage(BaseMessage, SecureMessage):

    def __init__(self, msg: Dict):
        super().__init__(msg=msg)
        # lazy
        self.__data: Optional[TransportableData] = None
        self.__keys: Optional[Dict] = None

    @property  # Override
    def data(self) -> TransportableData:
        ted = self.__data
        if ted is None:
            text = self.get('data')
            if text is None:
                assert False, 'message data not found: %s' % super().to_dict()
            elif not BaseMessage.is_broadcast(msg=self):
                # message content had been encrypted by a symmetric key,
                # so the data should be encoded here (with algorithm 'base64' as default).
                ted = TransportableData.parse(text)
            elif isinstance(text, str):
                # broadcast message content will not be encrypted (just encoded to JsON),
                # so return the string data directly
                ted = PlainData.create(string=text)  # JsON
            else:
                assert False, 'content data error: %s' % text
            self.__data = ted
        assert ted is not None, 'message data error: %s' % self.get('data')
        return ted

    @property  # Override
    def encrypted_keys(self) -> Optional[Dict]:
        keys = self.__keys
        if keys is None:
            keys = self.get('keys')
            if isinstance(keys, Dict):
                self.__keys = keys
            else:
                assert keys is None, 'message keys error: %s' % keys
                # TODO: get from 'key'
        return keys
