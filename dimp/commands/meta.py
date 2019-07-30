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

from mkm import ID, Meta

from ..protocol import ContentType, CommandContent


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

    def __init__(self, content: dict):
        super().__init__(content)
        # ID
        self.__identifier = ID(content['ID'])
        # meta
        self.__meta = Meta(content.get('meta'))

    #
    #   ID
    #
    @property
    def identifier(self) -> ID:
        return self.__identifier

    @identifier.setter
    def identifier(self, value: ID):
        self.__identifier = value
        if value is None:
            self.pop('ID', None)
        else:
            self['ID'] = value

    #
    #   Meta
    #
    @property
    def meta(self) -> Meta:
        return self.__meta

    @meta.setter
    def meta(self, value: Meta):
        self.__meta = value
        if value is None:
            self.pop('meta', None)
        else:
            self['meta'] = value

    #
    #   Factories
    #
    @classmethod
    def query(cls, identifier: str) -> CommandContent:
        content = {
            'type': ContentType.Command,
            'command': 'meta',
            'ID': identifier,
        }
        return MetaCommand(content)

    @classmethod
    def response(cls, identifier: str, meta: dict) -> CommandContent:
        content = {
            'type': ContentType.Command,
            'command': 'meta',
            'ID': identifier,
            'meta': meta,
        }
        return MetaCommand(content)
