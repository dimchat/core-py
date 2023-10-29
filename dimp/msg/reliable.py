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

from mkm.format import TransportableData

from dkd import ReliableMessage

from .secure import EncryptedMessage


"""
    Reliable Message signed by an asymmetric key
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    This class is used to sign the SecureMessage
    It contains a 'signature' field which signed with sender's private key

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
        },
        //-- signature
        signature: "..."   // base64_encode(asymmetric_sign(data))
    }
"""


class NetworkMessage(EncryptedMessage, ReliableMessage):

    def __init__(self, msg: Dict[str, Any]):
        super().__init__(msg=msg)
        # lazy
        self.__signature: Optional[TransportableData] = None

    @property  # Override
    def signature(self) -> bytes:
        ted = self.__signature
        if ted is None:
            base64 = self.get('signature')
            assert base64 is not None, 'message signature cannot be empty: %s' % self
            self.__signature = ted = TransportableData.parse(base64)
            assert ted is not None, 'failed to decode message signature: %s' % base64
        if ted is not None:
            return ted.data
