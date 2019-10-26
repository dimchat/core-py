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

from .command import Command, command_classes


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
        super().__init__(content)
        # value of 'ID' cannot be changed again
        self.__identifier = content['ID']
        # meta
        self.__meta = Meta(content.get('meta'))

    #
    #   ID
    #
    @property
    def identifier(self) -> str:
        # TODO: convert value to ID object
        return self.__identifier

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
    def query(cls, identifier: ID):
        content = {
            'command': Command.META,
            'ID': identifier,
        }
        return Command.new(content)

    @classmethod
    def response(cls, identifier: ID, meta: Meta):
        content = {
            'command': Command.META,
            'ID': identifier,
            'meta': meta,
        }
        return Command.new(content)


# register command class
command_classes[Command.META] = MetaCommand
