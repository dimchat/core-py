# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2022 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

from typing import Optional, Any, Dict

from dkd import ContentType, Content, ContentFactory, BaseContent

from ..protocol import Command, CommandFactory, GroupCommand

from .text import BaseTextContent
from .forward import SecretContent
from .array import ListContent
from .money import BaseMoneyContent, TransferMoneyContent
from .file import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent
from .page import WebPageContent
# from .customized import AppCustomizedContent

from .command import BaseCommand, command_name
from .meta import BaseMetaCommand
from .document import BaseDocumentCommand

from .history import BaseHistoryCommand
from .group import BaseGroupCommand
from .group import InviteGroupCommand, ExpelGroupCommand, JoinGroupCommand
from .group import QuitGroupCommand, QueryGroupCommand, ResetGroupCommand


class ContentFactoryBuilder(ContentFactory):

    def __init__(self, content_class):
        super().__init__()
        self.__class = content_class

    # Override
    def parse_content(self, content: Dict[str, Any]) -> Optional[Content]:
        # return self.__class(content=content)
        return self.__class(content)


class CommandFactoryBuilder(CommandFactory):

    def __init__(self, command_class):
        super().__init__()
        self.__class = command_class

    # Override
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        # return self.__class(content=content)
        return self.__class(content)


#
#   General Command Factory
#   ~~~~~~~~~~~~~~~~~~~~~~~
#
class GeneralCommandFactory(ContentFactory, CommandFactory):

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


class HistoryCommandFactory(GeneralCommandFactory):

    # Override
    def parse_command(self, content: Dict[str, Any]) -> Optional[Command]:
        return BaseHistoryCommand(content=content)


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
        return BaseGroupCommand(content=content)


def register_content_factories():
    """ Register core content factories """
    # Text
    Content.register(msg_type=ContentType.TEXT, factory=ContentFactoryBuilder(content_class=BaseTextContent))

    # File
    Content.register(msg_type=ContentType.FILE, factory=ContentFactoryBuilder(content_class=BaseFileContent))
    # Image
    Content.register(msg_type=ContentType.IMAGE, factory=ContentFactoryBuilder(content_class=ImageFileContent))
    # Audio
    Content.register(msg_type=ContentType.AUDIO, factory=ContentFactoryBuilder(content_class=AudioFileContent))
    # Video
    Content.register(msg_type=ContentType.VIDEO, factory=ContentFactoryBuilder(content_class=VideoFileContent))

    # Web Page
    Content.register(msg_type=ContentType.PAGE, factory=ContentFactoryBuilder(content_class=WebPageContent))

    # Money
    Content.register(msg_type=ContentType.MONEY, factory=ContentFactoryBuilder(content_class=BaseMoneyContent))
    Content.register(msg_type=ContentType.TRANSFER, factory=ContentFactoryBuilder(content_class=TransferMoneyContent))
    # ...

    # Command
    Content.register(msg_type=ContentType.COMMAND, factory=GeneralCommandFactory())

    # History Command
    Content.register(msg_type=ContentType.HISTORY, factory=HistoryCommandFactory())

    # Content Array
    Content.register(msg_type=ContentType.ARRAY, factory=ContentFactoryBuilder(content_class=ListContent))

    # # Application Customized
    # Content.register(msg_type=ContentType.APPLICATION,
    #                  factory=ContentFactoryBuilder(content_class=AppCustomizedContent))
    # Content.register(msg_type=ContentType.CUSTOMIZED,
    #                  factory=ContentFactoryBuilder(content_class=AppCustomizedContent))

    # Top-Secret
    Content.register(msg_type=ContentType.FORWARD, factory=ContentFactoryBuilder(content_class=SecretContent))

    # Unknown Content Type
    Content.register(msg_type=0, factory=ContentFactoryBuilder(content_class=BaseContent))


def register_command_factories():
    """ Register core command factories """
    # Meta Command
    Command.register(cmd=Command.META, factory=CommandFactoryBuilder(command_class=BaseMetaCommand))

    # Document Command
    Command.register(cmd=Command.DOCUMENT, factory=CommandFactoryBuilder(command_class=BaseDocumentCommand))

    # Group Commands
    Command.register(cmd='group', factory=GroupCommandFactory())
    Command.register(cmd=GroupCommand.INVITE, factory=CommandFactoryBuilder(command_class=InviteGroupCommand))
    Command.register(cmd=GroupCommand.EXPEL, factory=CommandFactoryBuilder(command_class=ExpelGroupCommand))
    Command.register(cmd=GroupCommand.JOIN, factory=CommandFactoryBuilder(command_class=JoinGroupCommand))
    Command.register(cmd=GroupCommand.QUIT, factory=CommandFactoryBuilder(command_class=QuitGroupCommand))
    Command.register(cmd=GroupCommand.QUERY, factory=CommandFactoryBuilder(command_class=QueryGroupCommand))
    Command.register(cmd=GroupCommand.RESET, factory=CommandFactoryBuilder(command_class=ResetGroupCommand))
