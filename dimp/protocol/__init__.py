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
    DIMP - Message Contents & Commands
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Define universal message types as contents and commands
"""

from typing import Optional

from dkd import ContentType, Content, BaseContent
from dkd.content import content_group

from .forward import ForwardContent
from .text import TextContent
from .file import FileContent, ImageContent, AudioContent, VideoContent
from .money import MoneyContent, TransferContent

from .command import Command, command_name
from .history import HistoryCommand
from .group import GroupCommand, InviteCommand, ExpelCommand, JoinCommand, QuitCommand, QueryCommand, ResetCommand

from .meta import MetaCommand
from .document import DocumentCommand


class ContentFactoryBuilder(Content.Factory):

    def __init__(self, content_class):
        super().__init__()
        self.__class = content_class

    def parse_content(self, content: dict) -> Optional[Content]:
        return self.__class(content=content)


class CommandFactoryBuilder(Command.Factory):

    def __init__(self, command_class):
        super().__init__()
        self.__class = command_class

    def parse_command(self, cmd: dict) -> Optional[Command]:
        return self.__class(cmd=cmd)


class CommandFactory(Content.Factory, Command.Factory):

    def __init__(self):
        super().__init__()

    def parse_content(self, content: dict) -> Optional[Content]:
        name = command_name(cmd=content)
        # get factory by command name
        factory = Command.factory(command=name)
        if factory is None:
            # check for group command
            if content_group(content=content) is not None:
                factory = Command.factory(command='group')
            if factory is None:
                factory = self
        return factory.parse_command(cmd=content)

    def parse_command(self, cmd: dict) -> Optional[Command]:
        return Command(cmd=cmd)


class HistoryCommandFactory(CommandFactory):

    def parse_command(self, cmd: dict) -> Optional[Command]:
        return HistoryCommand(cmd=cmd)


class GroupCommandFactory(HistoryCommandFactory):

    def parse_content(self, content: dict) -> Optional[Content]:
        name = command_name(cmd=content)
        # get factory by command name
        factory = Command.factory(command=name)
        if factory is None:
            factory = self
        return factory.parse_command(cmd=content)

    def parse_command(self, cmd: dict) -> Optional[Command]:
        return GroupCommand(cmd=cmd)


def register_content_factories():
    """ Register core content factories """
    Content.register(content_type=ContentType.FORWARD, factory=ContentFactoryBuilder(content_class=ForwardContent))
    Content.register(content_type=ContentType.TEXT, factory=ContentFactoryBuilder(content_class=TextContent))

    Content.register(content_type=ContentType.FILE, factory=ContentFactoryBuilder(content_class=FileContent))
    Content.register(content_type=ContentType.IMAGE, factory=ContentFactoryBuilder(content_class=ImageContent))
    Content.register(content_type=ContentType.AUDIO, factory=ContentFactoryBuilder(content_class=AudioContent))
    Content.register(content_type=ContentType.VIDEO, factory=ContentFactoryBuilder(content_class=VideoContent))

    # Content.register(content_type=ContentType.PAGE, factory=ContentFactoryBuilder(content_class=PageContent))

    Content.register(content_type=ContentType.MONEY, factory=ContentFactoryBuilder(content_class=MoneyContent))
    Content.register(content_type=ContentType.TRANSFER, factory=ContentFactoryBuilder(content_class=TransferContent))

    Content.register(content_type=ContentType.COMMAND, factory=CommandFactory())
    Content.register(content_type=ContentType.HISTORY, factory=HistoryCommandFactory())

    Content.register(content_type=0, factory=ContentFactoryBuilder(content_class=BaseContent))


def register_command_factories():
    """ Register core command factories """
    Command.register(command=Command.META, factory=CommandFactoryBuilder(command_class=MetaCommand))

    factory = CommandFactoryBuilder(command_class=DocumentCommand)
    Command.register(command=Command.DOCUMENT, factory=factory)
    Command.register(command='profile', factory=factory)
    Command.register(command='visa', factory=factory)
    Command.register(command='bulletin', factory=factory)

    Command.register(command='group', factory=GroupCommandFactory())
    Command.register(command=GroupCommand.INVITE, factory=CommandFactoryBuilder(command_class=InviteCommand))
    Command.register(command=GroupCommand.EXPEL, factory=CommandFactoryBuilder(command_class=ExpelCommand))
    Command.register(command=GroupCommand.JOIN, factory=CommandFactoryBuilder(command_class=JoinCommand))
    Command.register(command=GroupCommand.QUIT, factory=CommandFactoryBuilder(command_class=QuitCommand))
    Command.register(command=GroupCommand.QUERY, factory=CommandFactoryBuilder(command_class=QueryCommand))
    Command.register(command=GroupCommand.RESET, factory=CommandFactoryBuilder(command_class=ResetCommand))


def register_core_factories():
    register_content_factories()
    register_command_factories()


__all__ = [

    'ForwardContent', 'TextContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',

    'Command', 'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand',
    'QueryCommand', 'ResetCommand',

    'MetaCommand', 'DocumentCommand',

    'ContentFactoryBuilder', 'CommandFactoryBuilder',
    'register_core_factories',
]
