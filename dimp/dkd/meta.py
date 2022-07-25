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

from typing import Optional, Any, Dict

from mkm import ID, Meta

from ..protocol import MetaCommand

from .command import Command, BaseCommand


class BaseMetaCommand(BaseCommand, MetaCommand):
    """
        Meta Command
        ~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            cmd     : "meta", // command name
            ID      : "{ID}", // contact's ID
            meta    : {...}   // When meta is empty, means query meta for ID
        }
    """

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 cmd: Optional[str] = None,
                 identifier: Optional[ID] = None,
                 meta: Optional[Meta] = None):
        if content is None:
            if cmd is None:
                cmd = Command.META
            assert identifier is not None, 'ID should not be empty'
        super().__init__(content=content, cmd=cmd)
        self.__meta = meta
        if meta is not None:
            self['meta'] = meta.dictionary
        if identifier is not None:
            self['ID'] = str(identifier)

    #
    #   ID
    #
    @property  # Override
    def identifier(self) -> ID:
        return ID.parse(identifier=self.get('ID'))

    #
    #   Meta
    #
    @property  # Override
    def meta(self) -> Optional[Meta]:
        if self.__meta is None:
            info = self.get('meta')
            self.__meta = Meta.parse(meta=info)
        return self.__meta
