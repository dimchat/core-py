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

from dkd import MessageType, CommandContent

from mkm import ID, Meta


class MetaCommand(CommandContent):
    """
        Meta Command
        ~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "meta", // command name
            ID      : "{ID}", // contact's ID
            meta    : {...}   // When meta is empty, means query meta for ID
        }
    """

    #
    #   ID
    #
    @property
    def identifier(self) -> ID:
        value = self.get('ID')
        if value:
            return ID(value)

    @identifier.setter
    def identifier(self, value: str):
        if value:
            self['ID'] = value
        else:
            self.pop('ID')

    #
    #   Meta
    #
    @property
    def meta(self) -> Meta:
        value = self.get('meta')
        if value:
            return Meta(value)

    @meta.setter
    def meta(self, value: dict):
        if value:
            self['meta'] = value
        else:
            self.pop('meta')

    #
    #   Factories
    #
    @classmethod
    def query(cls, identifier: str) -> CommandContent:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'meta',
            'ID': identifier,
        }
        return MetaCommand(content)

    @classmethod
    def response(cls, identifier: str, meta: dict) -> CommandContent:
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'meta',
            'ID': identifier,
            'meta': meta,
        }
        return MetaCommand(content)
