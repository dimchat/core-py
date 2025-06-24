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

from abc import ABC
from typing import Optional, Any, Dict

from mkm.types import Converter
from dkd import Envelope

from ..protocol import Command
from ..protocol import ReceiptCommand
from .commands import BaseCommand


class BaseReceiptCommand(BaseCommand, ReceiptCommand, ABC):
    """
        Receipt Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x88),
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
                 text: str = None, origin: Dict[str, Any] = None):
        if content is None:
            # 1. new command with text & origin info
            assert text is not None, 'receipt text should not be None, %s' % origin
            cmd = Command.RECEIPT
            super().__init__(cmd=cmd)
            # text message
            self['text'] = text
            # original envelope of message responding to,
            # includes 'sn' and 'signature'
            if origin is not None:
                assert not (len(origin) == 0 or
                            'data' in origin or
                            'key' in origin or
                            'keys' in origin or
                            'meta' in origin or
                            'visa' in origin), 'impure envelope: %s' % origin
                self['origin'] = origin
        else:
            # 2. command info from network
            assert text is None and origin is None, 'params error: %s, %s, %s' % (content, text, origin)
            # create with command content
            super().__init__(content=content)
        # lazy load
        self.__env = None

    # -------- setters/getters

    @property  # Override
    def text(self) -> str:
        return self.get_str(key='text', default='')

    @property  # protected
    def origin(self) -> Optional[Dict]:
        return self.get('origin')

    @property  # Override
    def original_envelope(self) -> Optional[Envelope]:
        if self.__env is None:
            # origin: { sender: "...", receiver: "...", time: 0 }
            self.__env = Envelope.parse(envelope=self.origin)
        return self.__env

    @property  # Override
    def original_sn(self) -> Optional[int]:
        origin = self.origin
        if origin is not None:
            sn = origin.get('sn')
            return Converter.get_int(value=sn, default=None)

    @property  # Override
    def original_signature(self) -> Optional[str]:
        origin = self.origin
        if origin is not None:
            signature = origin.get('signature')
            return Converter.get_str(value=signature, default=None)
