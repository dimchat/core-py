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

from .base import BaseContent, BaseCommand
from .contents import BaseTextContent, ListContent, SecretContent, AppCustomizedContent
from .contents import WebPageContent, BaseMoneyContent, TransferMoneyContent
from .files import BaseFileContent, ImageFileContent, AudioFileContent, VideoFileContent
from .commands import BaseMetaCommand, BaseDocumentCommand
from .receipt import BaseReceiptCommand

from .groups import BaseHistoryCommand, BaseGroupCommand
from .groups import InviteGroupCommand, ExpelGroupCommand, JoinGroupCommand
from .groups import QuitGroupCommand, QueryGroupCommand, ResetGroupCommand
from .groups import HireGroupCommand, FireGroupCommand, ResignGroupCommand


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
    #   Contents
    #
    'BaseContent',
    'BaseTextContent', 'SecretContent', 'ListContent',
    'BaseMoneyContent', 'TransferMoneyContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'WebPageContent', 'AppCustomizedContent',

    'BaseCommand',
    'BaseMetaCommand', 'BaseDocumentCommand',
    'BaseReceiptCommand',

    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand',
    'QuitGroupCommand', 'QueryGroupCommand', 'ResetGroupCommand',
    'HireGroupCommand', 'FireGroupCommand', 'ResignGroupCommand',
]
