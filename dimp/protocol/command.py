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

from dkd import Content, ContentType


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
        elif cls is Command:
            if isinstance(cmd, Command):
                # return Command object directly
                return cmd
            # get class by command name
            clazz = cls.command_class(command=cmd['command'])
            if clazz is not None:
                # noinspection PyTypeChecker
                return clazz.__new__(clazz, cmd)
        # subclass or default Command(dict)
        return super().__new__(cls, cmd)

    def __init__(self, cmd: dict):
        if self is cmd:
            # no need to init again
            return
        super().__init__(cmd)
        # command name
        self.__command: str = None

    @property
    def command(self) -> str:
        if self.__command is None:
            self.__command = self['command']
        return self.__command

    #
    #   Factory
    #
    @classmethod
    def new(cls, content: dict=None, command: str=None):
        """
        Create command message content with 'command' as name

        :param content: command info
        :param command: command name
        :return: Command object
        """
        if content is None:
            # create empty content
            content = {}
        # set content type: 'Command'
        if 'type' not in content:
            content['type'] = ContentType.Command
        # set command name
        if command is not None:
            content['command'] = command
        # new Command(dict)
        return super().new(content=content)

    #
    #   Runtime
    #
    __command_classes = {}  # class map

    @classmethod
    def register(cls, command: str, command_class=None) -> bool:
        """
        Register command class with command name

        :param command:  command name
        :param command_class: if command class is None, then remove with type
        :return: False on error
        """
        if command_class is None:
            cls.__command_classes.pop(command, None)
        elif issubclass(command_class, Command):
            cls.__command_classes[command] = command_class
        else:
            raise TypeError('%s must be subclass of Command' % command_class)
        return True

    @classmethod
    def command_class(cls, command: str):
        """
        Get command class with command name

        :param command: command name
        :return: command class
        """
        return cls.__command_classes.get(command)


# register content class with type
Content.register(content_type=ContentType.Command, content_class=Command)
