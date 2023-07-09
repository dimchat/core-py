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
    Receipt Protocol
    ~~~~~~~~~~~~~~~~

    As receipt returned to sender to proofing the message's received
"""

from typing import Optional, Union, Any, Dict

from mkm.crypto import base64_encode
from dkd import ContentType
from dkd import Envelope

from ..protocol import ReceiptCommand, ReceiptCommandMixIn
from .commands import BaseCommand


class BaseReceipt(BaseCommand, ReceiptCommand):
    """
        Receipt Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 456,

            command : "receipt",
            text    : "...",  // text message
            origin  : {       // original message envelope
                sender    : "...",
                receiver  : "...",
                time      : 0,

                sn        : 123,
                signature : "..."
            }
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 msg_type: Union[int, ContentType] = 0,
                 text: str = None,
                 envelope: Envelope = None, sn: int = 0, signature: Union[str, bytes] = None):
        if content is None:
            assert msg_type > 0 and text is not None, 'receipt error: type=%s, text="%s"' % (msg_type, text)
            super().__init__(msg_type=msg_type, cmd=self.RECEIPT)
            # text message
            self['text'] = text
            # original envelope
            self.__env = envelope
            # envelope of the message responding to
            if envelope is None:
                origin = {}
            else:
                origin = envelope.dictionary
            # sn of the message responding to
            if sn > 0:
                origin['sn'] = sn
            # signature of the message responding to
            if isinstance(signature, str):
                origin['signature'] = signature
            elif isinstance(signature, bytes):
                origin['signature'] = base64_encode(data=signature)
            if len(origin) > 0:
                self['origin'] = origin
        else:
            # create with command content
            super().__init__(content=content)
            # lazy load
            self.__env = None

    # -------- setters/getters

    @property
    def text(self) -> str:
        return self.get('text', default='')

    @property  # protected
    def origin(self) -> Optional[Dict]:
        return self.get('origin')

    @property
    def original_envelope(self) -> Optional[Envelope]:
        if self.__env is None:
            # origin: { sender: "...", receiver: "...", time: 0 }
            origin = self.origin
            if origin is not None and 'sender' in origin:
                self.__env = Envelope.parse(envelope=origin)
        return self.__env

    @property
    def original_sn(self) -> Optional[int]:
        origin = self.origin
        if origin is not None:
            return origin.get('sn')

    @property
    def original_signature(self) -> Optional[str]:
        origin = self.origin
        if origin is not None:
            return origin.get('signature')


class BaseReceiptCommand(BaseReceipt, ReceiptCommandMixIn):

    @classmethod
    def from_text(cls, text: str, envelope: Envelope = None, sn: int = 0, signature: Union[str, bytes] = None):
        return cls(msg_type=ContentType.COMMAND, text=text, envelope=envelope, sn=sn, signature=signature)
