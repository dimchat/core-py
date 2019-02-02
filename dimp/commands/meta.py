# -*- coding: utf-8 -*-
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

from dkd.contents import serial_number

from mkm import ID, Meta
from dkd import MessageType, CommandContent


class MetaCommand(CommandContent):

    def __init__(self, content: dict):
        super().__init__(content)
        # ID
        self.identifier = ID(content['ID'])
        # meta
        if 'meta' in content:
            self.meta = Meta(content['meta'])
        else:
            self.meta = None

    @classmethod
    def query(cls, identifier: ID) -> CommandContent:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'meta',
            'ID': identifier,
        }
        return MetaCommand(content)

    @classmethod
    def response(cls, identifier: ID, meta: Meta) -> CommandContent:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'meta',
            'ID': identifier,
            'meta': meta,
        }
        return MetaCommand(content)
