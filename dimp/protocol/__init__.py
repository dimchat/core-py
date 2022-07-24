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

from typing import Optional, Any, Dict

from dkd import ContentType, Content, ContentFactory, BaseContent

from .forward import ForwardContent
from .text import TextContent
from .file import FileContent, ImageContent, AudioContent, VideoContent
from .money import MoneyContent, TransferContent

from .command import Command, CommandFactory, command_name
from .command import BaseCommand
from .history import HistoryCommand
from .group import GroupCommand, InviteCommand, ExpelCommand, JoinCommand, QuitCommand, QueryCommand, ResetCommand

from .meta import MetaCommand
from .document import DocumentCommand


class ContentFactoryBuilder(ContentFactory):

    def __init__(self, content_class):
        super().__init__()
        self.__class = content_class

    # Override
    def parse_content(self, content: Dict[str, Any]) -> Optional[Content]:
        return self.__class(content=content)


class CommandFactoryBuilder(CommandFactory):

    def __init__(self, command_class):
        super().__init__()
        self.__class = command_class

    # Override
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        return self.__class(content=content)


class CommandContentFactory(ContentFactory, CommandFactory):

    def __init__(self):
        super().__init__()

    # Override
    def parse_content(self, content: Dict[str, Any]) -> Optional[Content]:
        name = command_name(content=content)
        # get factory by command name
        factory = Command.factory(cmd=name)
        if factory is None:
            # check for group command
            if 'group' in content:
                factory = Command.factory(cmd='group')
            if factory is None:
                factory = self
        return factory.parse_command(content=content)

    # Override
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        return BaseCommand(content=content)


class HistoryCommandFactory(CommandContentFactory):

    # Override
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        return HistoryCommand(content=content)


class GroupCommandFactory(HistoryCommandFactory):

    # Override
    def parse_content(self, content: Dict[str, Any]) -> Optional[Content]:
        name = command_name(content=content)
        # get factory by command name
        factory = Command.factory(cmd=name)
        if factory is None:
            factory = self
        return factory.parse_command(content=content)

    # Override
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        return GroupCommand(content=content)


def register_content_factories():
    """ Register core content factories """
    Content.register(msg_type=ContentType.FORWARD, factory=ContentFactoryBuilder(content_class=ForwardContent))
    Content.register(msg_type=ContentType.TEXT, factory=ContentFactoryBuilder(content_class=TextContent))

    Content.register(msg_type=ContentType.FILE, factory=ContentFactoryBuilder(content_class=FileContent))
    Content.register(msg_type=ContentType.IMAGE, factory=ContentFactoryBuilder(content_class=ImageContent))
    Content.register(msg_type=ContentType.AUDIO, factory=ContentFactoryBuilder(content_class=AudioContent))
    Content.register(msg_type=ContentType.VIDEO, factory=ContentFactoryBuilder(content_class=VideoContent))

    # Content.register(msg_type=ContentType.PAGE, factory=ContentFactoryBuilder(content_class=PageContent))

    Content.register(msg_type=ContentType.MONEY, factory=ContentFactoryBuilder(content_class=MoneyContent))
    Content.register(msg_type=ContentType.TRANSFER, factory=ContentFactoryBuilder(content_class=TransferContent))

    Content.register(msg_type=ContentType.COMMAND, factory=CommandContentFactory())
    Content.register(msg_type=ContentType.HISTORY, factory=HistoryCommandFactory())

    Content.register(msg_type=0, factory=ContentFactoryBuilder(content_class=BaseContent))


def register_command_factories():
    """ Register core command factories """
    # meta command
    Command.register(cmd=Command.META, factory=CommandFactoryBuilder(command_class=MetaCommand))
    # document command
    Command.register(cmd=Command.DOCUMENT, factory=CommandFactoryBuilder(command_class=DocumentCommand))
    # group commands
    Command.register(cmd='group', factory=GroupCommandFactory())
    Command.register(cmd=GroupCommand.INVITE, factory=CommandFactoryBuilder(command_class=InviteCommand))
    Command.register(cmd=GroupCommand.EXPEL, factory=CommandFactoryBuilder(command_class=ExpelCommand))
    Command.register(cmd=GroupCommand.JOIN, factory=CommandFactoryBuilder(command_class=JoinCommand))
    Command.register(cmd=GroupCommand.QUIT, factory=CommandFactoryBuilder(command_class=QuitCommand))
    Command.register(cmd=GroupCommand.QUERY, factory=CommandFactoryBuilder(command_class=QueryCommand))
    Command.register(cmd=GroupCommand.RESET, factory=CommandFactoryBuilder(command_class=ResetCommand))


__all__ = [

    'ForwardContent', 'TextContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',

    'Command', 'BaseCommand', 'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand',
    'QueryCommand', 'ResetCommand',

    'MetaCommand', 'DocumentCommand',

    'ContentFactoryBuilder', 'CommandFactoryBuilder',

    # register_core_factories
    'register_content_factories', 'register_command_factories',
]
