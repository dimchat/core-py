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
    Meta Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~

    1. contains 'ID' only, means query meta for ID
    2. contains 'meta' (must match), means reply
"""

from dkd import ContentType

from ..protocol import Command


class ReceiptCommand(Command):
    """
        Receipt Command
        ~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "receipt", // command name
            message : "...",
        }
    """

    #
    #   message
    #
    @property
    def message(self) -> str:
        return self.get('message')

    @message.setter
    def message(self, value: str):
        if value is None:
            self.pop('message', None)
        else:
            self['message'] = value

    #
    #   Factory
    #
    @classmethod
    def receipt(cls, message: str) -> Command:
        content = {
            'type': ContentType.Command,
            'command': 'receipt',
            'message': message,
        }
        return ReceiptCommand(content)
