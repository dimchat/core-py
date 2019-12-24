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

from typing import Optional

from mkm import ID, Meta

from .command import Command


class MetaCommand(Command):
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

    def __new__(cls, cmd: dict):
        """
        Create meta command

        :param cmd: command info
        :return: MetaCommand object
        """
        if cmd is None:
            return None
        elif cls is MetaCommand:
            if isinstance(cmd, MetaCommand):
                # return MetaCommand object directly
                return cmd
        # new MetaCommand(dict)
        return super().__new__(cls, cmd)

    def __init__(self, content: dict):
        if self is content:
            # no need to init again
            return
        super().__init__(content)
        # lazy
        self.__meta: Meta = None

    #
    #   ID
    #
    @property
    def identifier(self) -> str:
        return self['ID']

    #
    #   Meta
    #
    @property
    def meta(self) -> Optional[Meta]:
        if self.__meta is None:
            self.__meta = Meta(self.get('meta'))
        return self.__meta

    @meta.setter
    def meta(self, value: Meta):
        if value is None:
            self.pop('meta', None)
        else:
            self['meta'] = value
        self.__meta = value

    #
    #   Factories
    #
    @classmethod
    def new(cls, content: dict=None, identifier: ID=None, meta: Meta=None):
        """
        Create meta command for entity

        :param content:    command info
        :param identifier: entity ID
        :param meta:       meta info
        :return: MetaCommand object
        """
        if content is None:
            # create empty content
            content = {}
        # set command name: 'meta'
        if 'command' not in content:
            content['command'] = Command.META
        # set entity ID
        if identifier is not None:
            content['ID'] = identifier
        # set entity meta
        if meta is not None:
            content['meta'] = meta
        # new MetaCommand(dict)
        return super().new(content=content)

    @classmethod
    def query(cls, identifier: ID):
        return cls.new(identifier=identifier)

    @classmethod
    def response(cls, identifier: ID, meta: Meta):
        return cls.new(identifier=identifier, meta=meta)


# register command class
Command.register(command=Command.META, command_class=MetaCommand)
