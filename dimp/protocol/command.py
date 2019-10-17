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

from typing import Union

from dkd import Content, ContentType
from dkd.content import message_content_classes


class Command(Content):
    """
        Command Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "...", // command name
            extra   : info   // command parameters
        }
    """

    # -------- command names begin --------
    HANDSHAKE = 'handshake'
    RECEIPT = 'receipt'
    META = 'meta'
    PROFILE = 'profile'
    # -------- command names end --------

    def __new__(cls, cmd: dict):
        """
        Create command

        :param cmd: command info
        :return: Command object
        """
        if cmd is None:
            return None
        elif isinstance(cmd, Command):
            # return Command object directly
            return cmd
        elif cls is Command:
            # get class by command name
            clazz = command_classes.get(cmd['command'])
            if clazz is not None:
                assert issubclass(clazz, Command), '%s must be sub-class of Command' % clazz
                return clazz(cmd)
        # new Command(dict)
        return super().__new__(cls, cmd)

    def __init__(self, content: dict):
        super().__init__(content)
        # value of 'command' cannot be changed again
        self.__command = content['command']

    @property
    def command(self) -> str:
        return self.__command

    #
    #   Factory
    #
    @classmethod
    def new(cls, command: Union[str, dict]):
        if isinstance(command, str):
            content = {
                'type': ContentType.Command,
                'command': command,
            }
        elif isinstance(command, dict):
            content = command
            if 'type' not in content:
                content['type'] = ContentType.Command
            assert 'command' in content, 'command error: %s' % command
        else:
            raise TypeError('command argument error: %s' % command)
        # new Command(dict)
        return cls(content)


"""
    Command Classes Map
"""

command_classes = {
}

# register content class
message_content_classes[ContentType.Command] = Command
