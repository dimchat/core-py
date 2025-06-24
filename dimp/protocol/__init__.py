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

from mkm.types import *
from mkm.format import *
from mkm.crypto import *

from mkm.protocol import *
from dkd.protocol import *

from mkm import ANYWHERE, EVERYWHERE, ANYONE, EVERYONE, FOUNDER

from .types import MetaType, DocumentType, ContentType
from .docs import Visa, Bulletin

from .contents import TextContent, ArrayContent, ForwardContent
from .contents import PageContent, NameCard
from .files import FileContent, ImageContent, AudioContent, VideoContent
from .money import MoneyContent, TransferContent
from .quote import QuoteContent, CombineContent

from .commands import Command, CommandFactory
from .commands import MetaCommand, DocumentCommand
from .receipt import ReceiptCommand

from .groups import HistoryCommand, GroupCommand
from .groups import InviteCommand, ExpelCommand, JoinCommand, QuitCommand, QueryCommand, ResetCommand
from .groups import HireCommand, FireCommand, ResignCommand

# from .commands import CommandHelper
# from .helpers import CommandExtensions


__all__ = [

    'URI', 'DateTime',
    'TransportableData', 'PortableNetworkFile',

    'CryptographyKey',
    'EncryptKey', 'DecryptKey', 'SignKey', 'VerifyKey',
    'SymmetricKey', 'AsymmetricKey',
    'PrivateKey', 'PublicKey',

    #
    #   MingKeMing
    #

    'EntityType',
    'Address',   # 'AddressFactory',
    'ID',        # 'IDFactory',
    'Meta',      # 'MetaFactory',
    'Document',  # 'DocumentFactory',
    'Visa', 'Bulletin',

    'ANYWHERE', 'EVERYWHERE', 'ANYONE', 'EVERYONE', 'FOUNDER',

    'MetaType', 'DocumentType',

    #
    #   DaoKeDao
    #

    'ContentType',
    'Content',          # 'ContentFactory',
    'Envelope',         # 'EnvelopeFactory',
    'Message',
    'InstantMessage',   # 'InstantMessageFactory',
    'SecureMessage',    # 'SecureMessageFactory',
    'ReliableMessage',  # 'ReliableMessageFactory',

    # contents
    'TextContent', 'ArrayContent', 'ForwardContent',
    'PageContent', 'NameCard',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'MoneyContent', 'TransferContent',
    'QuoteContent', 'CombineContent',

    # commands
    'Command',          # 'CommandFactory',
    'MetaCommand', 'DocumentCommand',
    'ReceiptCommand',

    # group history
    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'QueryCommand', 'ResetCommand',
    'HireCommand', 'FireCommand', 'ResignCommand',

    #
    #   Plugins
    #

    # 'CommandHelper', 'CommandExtensions',

]
