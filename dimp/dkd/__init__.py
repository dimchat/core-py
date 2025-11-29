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

from ..protocol.base import BaseContent
from ..protocol.contents import BaseTextContent, WebPageContent, NameCardContent
from ..protocol.forward import SecretContent, CombineForwardContent, ListContent
from ..protocol.files import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent
from ..protocol.assets import BaseMoneyContent, TransferMoneyContent
from ..protocol.quote import BaseQuoteContent
from ..protocol.app import AppCustomizedContent

from ..protocol.base import BaseCommand
from ..protocol.commands import BaseMetaCommand, BaseDocumentCommand
from ..protocol.receipt import BaseReceiptCommand

from ..protocol.groups import BaseHistoryCommand, BaseGroupCommand
from ..protocol.groups import InviteGroupCommand, ExpelGroupCommand
from ..protocol.groups import JoinGroupCommand, QuitGroupCommand, ResetGroupCommand

# from ..protocol.base import CommandHelper
# from ..protocol.helpers import CommandExtensions

__all__ = [

    #
    #   Protocol
    #

    'ContentType',
    'Content',
    'Envelope',
    'Message',
    'InstantMessage', 'SecureMessage', 'ReliableMessage',

    # contents
    'TextContent', 'PageContent', 'NameCard',
    'ForwardContent', 'CombineContent', 'ArrayContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'MoneyContent', 'TransferContent',
    'QuoteContent',
    'CustomizedContent',

    # commands
    'Command',
    'MetaCommand', 'DocumentCommand',
    'ReceiptCommand',

    # group history
    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'ResetCommand',

    #
    #   Factories
    #

    'ContentFactory',
    'EnvelopeFactory',
    'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',

    #
    #   Extends
    #

    # contents
    'BaseContent',
    'BaseTextContent', 'WebPageContent', 'NameCardContent',
    'SecretContent', 'CombineForwardContent', 'ListContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'BaseMoneyContent', 'TransferMoneyContent',
    'BaseQuoteContent',
    'AppCustomizedContent',

    # commands
    'BaseCommand',
    'BaseMetaCommand', 'BaseDocumentCommand',
    'BaseReceiptCommand',

    # group history
    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand',
    'JoinGroupCommand', 'QuitGroupCommand', 'ResetGroupCommand',

    #
    #   Plugins
    #

    # 'CommandHelper', 'CommandExtensions',

]
