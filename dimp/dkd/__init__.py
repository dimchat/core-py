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

from dkd import *

from .text import BaseTextContent
from .forward import SecretContent
from .array import ListContent
from .money import BaseMoneyContent, TransferMoneyContent
from .file import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent
from .page import WebPageContent
from .customized import AppCustomizedContent

from .command import BaseCommand
from .meta import BaseMetaCommand
from .document import BaseDocumentCommand

from .history import BaseHistoryCommand
from .group import BaseGroupCommand
from .group import InviteGroupCommand, ExpelGroupCommand, JoinGroupCommand
from .group import QuitGroupCommand, QueryGroupCommand, ResetGroupCommand

from .factories import ContentFactoryBuilder, CommandFactoryBuilder
from .factories import GeneralCommandFactory, HistoryCommandFactory, GroupCommandFactory
from .factories import register_content_factories, register_command_factories


__all__ = [

    #
    #   Protocol
    #
    'ContentType', 'Content', 'ContentFactory',
    'Envelope', 'EnvelopeFactory',
    'Message', 'InstantMessage', 'SecureMessage', 'ReliableMessage',
    'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',
    'InstantMessageDelegate', 'SecureMessageDelegate', 'ReliableMessageDelegate',

    #
    #   Core
    #
    'BaseContent',
    'MessageEnvelope', 'MessageEnvelopeFactory',
    'BaseMessage',
    'PlainMessage', 'PlainMessageFactory',
    'EncryptedMessage', 'EncryptedMessageFactory',
    'NetworkMessage', 'NetworkMessageFactory',

    #
    #   Contents
    #
    'BaseTextContent', 'SecretContent', 'ListContent',
    'BaseMoneyContent', 'TransferMoneyContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'WebPageContent', 'AppCustomizedContent',

    'BaseCommand',
    'BaseMetaCommand', 'BaseDocumentCommand',

    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand',
    'QuitGroupCommand', 'QueryGroupCommand', 'ResetGroupCommand',

    'ContentFactoryBuilder', 'CommandFactoryBuilder',
    'GeneralCommandFactory', 'HistoryCommandFactory', 'GroupCommandFactory',

    'register_message_factories',
    'register_content_factories',
    'register_command_factories',
]
