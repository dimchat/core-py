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

from dkd.protocol import *

from ..protocol import *

from ..protocol.base import BaseContent, BaseCommand
# from ..protocol.base import CommandHelper, GeneralCommandHelper
from ..protocol.contents import BaseTextContent, WebPageContent, NameCardContent
from ..protocol.assets import BaseMoneyContent, TransferMoneyContent
from ..protocol.files import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent
from ..protocol.forward import SecretContent, CombineForwardContent, ListContent
from ..protocol.quote import BaseQuoteContent
# from ..protocol.quote import QuoteHelper, QuotePurifier
from ..protocol.commands import BaseMetaCommand, BaseDocumentCommand
from ..protocol.receipt import BaseReceiptCommand
from ..protocol.groups import BaseHistoryCommand, BaseGroupCommand
from ..protocol.groups import InviteGroupCommand, ExpelGroupCommand
from ..protocol.groups import JoinGroupCommand, QuitGroupCommand, ResetGroupCommand

from .envelope import MessageEnvelope
from .base import BaseMessage
from .instant import PlainMessage
from .secure import EncryptedMessage
from .reliable import NetworkMessage


__all__ = [

    #
    #   Protocol
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
    #   Extends
    #

    'ContentType',

    'Command', 'CommandFactory',
    # 'CommandHelper', 'GeneralCommandHelper',

    'TextContent', 'PageContent', 'NameCard',
    'MoneyContent', 'TransferContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'ForwardContent', 'CombineContent', 'ArrayContent',
    'QuoteContent',  # 'QuoteHelper', 'QuotePurifier',

    'MetaCommand', 'DocumentCommand',
    'ReceiptCommand',

    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'ResetCommand',

    #
    #   Implementations
    #

    'BaseContent', 'BaseCommand',

    'BaseTextContent', 'WebPageContent', 'NameCardContent',
    'BaseMoneyContent', 'TransferMoneyContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'SecretContent', 'CombineForwardContent', 'ListContent',
    'BaseQuoteContent',

    'BaseMetaCommand', 'BaseDocumentCommand',
    'BaseReceiptCommand',
    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand', 'QuitGroupCommand', 'ResetGroupCommand',

    #
    #   Messages
    #

    'MessageEnvelope',
    'BaseMessage',
    'PlainMessage', 'EncryptedMessage', 'NetworkMessage',

]
