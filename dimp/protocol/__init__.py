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

from mkm.protocol import *
from dkd.protocol import *

from .version import MetaType, DocumentType
from .docs import Visa, Bulletin

from .types import ContentType

from .base import Command, CommandFactory
# from .base import BaseContent, BaseCommand
# from .base import CommandHelper, GeneralCommandHelper

from .contents import TextContent, PageContent, NameCard
# from .contents import BaseTextContent, WebPageContent, NameCardContent

from .assets import MoneyContent, TransferContent
# from .assets import BaseMoneyContent, TransferMoneyContent

from .files import FileContent, ImageContent, AudioContent, VideoContent
# from .files import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent

from .forward import ForwardContent, CombineContent, ArrayContent
# from .forward import SecretContent, CombineForwardContent, ListContent

from .quote import QuoteContent
# from .quote import BaseQuoteContent
# from .quote import QuoteHelper, QuotePurifier

from .commands import MetaCommand, DocumentCommand
# from .commands import BaseMetaCommand, BaseDocumentCommand

from .receipt import ReceiptCommand
# from .receipt import BaseReceiptCommand

from .groups import HistoryCommand, GroupCommand
from .groups import InviteCommand, ExpelCommand, JoinCommand, QuitCommand, ResetCommand
# from .groups import BaseHistoryCommand, BaseGroupCommand
# from .groups import InviteGroupCommand, ExpelGroupCommand, JoinGroupCommand, QuitGroupCommand, ResetGroupCommand


__all__ = [

    #
    #   MingKeMing
    #

    'EntityType',
    'Address', 'ID',
    'Meta', 'TAI', 'Document',

    'AddressFactory', 'IDFactory',
    'MetaFactory', 'DocumentFactory',

    'ANYWHERE', 'EVERYWHERE',
    'ANYONE', 'EVERYONE', 'FOUNDER',
    # 'BroadcastAddress', 'Identifier',

    # 'AddressHelper', 'IDHelper',
    # 'MetaHelper', 'DocumentHelper',
    # 'AccountExtensions', 'shared_account_extensions',

    #
    #   DaoKeDao
    #

    'Content', 'Envelope',
    'Message',
    'InstantMessage', 'SecureMessage', 'ReliableMessage',

    'ContentFactory', 'EnvelopeFactory',
    'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',

    # 'ContentHelper', 'EnvelopeHelper',
    # 'InstantMessageHelper', 'SecureMessageHelper', 'ReliableMessageHelper',
    # 'MessageExtensions', 'shared_message_extensions',

    #
    #  Extends
    #

    'MetaType',
    'DocumentType',
    'Visa', 'Bulletin',

    'ContentType',

    'Command', 'CommandFactory',
    # 'CommandHelper', 'GeneralCommandHelper',

    #
    #  Content Extends
    #

    'TextContent', 'PageContent', 'NameCard',
    'MoneyContent', 'TransferContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'ForwardContent', 'CombineContent', 'ArrayContent',
    'QuoteContent',  # 'QuoteHelper', 'QuotePurifier',

    #
    #  Command Extends
    #

    'MetaCommand', 'DocumentCommand',
    'ReceiptCommand',

    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'ResetCommand',

    #
    #   Implementations
    #

    # 'BaseContent', 'BaseCommand',

    # 'BaseTextContent', 'WebPageContent', 'NameCardContent',
    # 'BaseMoneyContent', 'TransferMoneyContent',
    # 'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    # 'SecretContent', 'CombineForwardContent', 'ListContent',
    # 'BaseQuoteContent',

    # 'BaseMetaCommand', 'BaseDocumentCommand',
    # 'BaseReceiptCommand',
    # 'BaseHistoryCommand', 'BaseGroupCommand',
    # 'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand', 'QuitGroupCommand', 'ResetGroupCommand',

]
