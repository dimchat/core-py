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
from ..protocol import *

from .base import BaseContent, BaseCommand
from .contents import BaseTextContent, ListContent, SecretContent
from .contents import WebPageContent, NameCardContent
from .files import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent
from .money import BaseMoneyContent, TransferMoneyContent
from .customized import AppCustomizedContent

from .commands import BaseMetaCommand, BaseDocumentCommand
from .receipt import BaseReceipt, BaseReceiptCommand

from .groups import BaseHistoryCommand, BaseGroupCommand
from .groups import InviteGroupCommand, ExpelGroupCommand, JoinGroupCommand
from .groups import QuitGroupCommand, QueryGroupCommand, ResetGroupCommand
from .group_admins import HireGroupCommand, FireGroupCommand, ResignGroupCommand

from .factory import CommandGeneralFactory, CommandFactoryManager


__all__ = [

    #
    #   Protocol
    #
    'ContentType', 'Content', 'ContentFactory',
    'Envelope', 'EnvelopeFactory',
    'Message',
    'InstantMessage', 'InstantMessageFactory',
    'SecureMessage', 'SecureMessageFactory',
    'ReliableMessage', 'ReliableMessageFactory',

    'InstantMessageDelegate', 'SecureMessageDelegate', 'ReliableMessageDelegate',
    'MessageGeneralFactory', 'MessageFactoryManager',

    'TextContent', 'ArrayContent', 'ForwardContent',
    'PageContent', 'NameCard',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'MoneyContent', 'TransferContent',
    'CustomizedContent',

    'Command', 'CommandFactory',
    'MetaCommand', 'DocumentCommand',
    'ReceiptCommand', 'ReceiptCommandMixIn',

    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'QueryCommand', 'ResetCommand',
    'HireCommand', 'FireCommand', 'ResignCommand',

    #
    #   Contents
    #
    'BaseContent',
    'BaseTextContent', 'ListContent', 'SecretContent',
    'WebPageContent', 'NameCardContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'BaseMoneyContent', 'TransferMoneyContent',
    'AppCustomizedContent',

    #
    #   Commands
    #
    'BaseCommand',
    'BaseMetaCommand', 'BaseDocumentCommand',
    'BaseReceipt', 'BaseReceiptCommand',

    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand',
    'QuitGroupCommand', 'QueryGroupCommand', 'ResetGroupCommand',
    'HireGroupCommand', 'FireGroupCommand', 'ResignGroupCommand',

    'CommandGeneralFactory', 'CommandFactoryManager',
]
