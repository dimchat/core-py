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

from mkm.types import URI, DateTime
from mkm.format import TransportableData, PortableNetworkFile
from mkm.crypto import SymmetricKey, AsymmetricKey
from mkm.crypto import EncryptKey, DecryptKey
from mkm.crypto import SignKey, VerifyKey
from mkm.crypto import PublicKey, PrivateKey

from mkm.protocol import *
from dkd.protocol import *

from mkm import ANYWHERE, EVERYWHERE, ANYONE, EVERYONE, FOUNDER
# from dkd import InstantMessageDelegate, SecureMessageDelegate, ReliableMessageDelegate

from .docs import Visa, Bulletin

from .contents import TextContent, ArrayContent, ForwardContent
from .contents import PageContent, NameCard
from .files import FileContent, ImageContent, AudioContent, VideoContent
from .money import MoneyContent, TransferContent
from .customized import CustomizedContent

from .commands import Command, CommandFactory
from .commands import MetaCommand, DocumentCommand
from .receipt import ReceiptCommand, ReceiptCommandMixIn

from .groups import HistoryCommand, GroupCommand
from .groups import InviteCommand, ExpelCommand, JoinCommand, QuitCommand, QueryCommand, ResetCommand
from .groups import HireCommand, FireCommand, ResignCommand


__all__ = [

    'URI', 'DateTime',
    'TransportableData', 'PortableNetworkFile',

    'SymmetricKey', 'AsymmetricKey',
    'EncryptKey', 'DecryptKey',
    'SignKey', 'VerifyKey',
    'PublicKey', 'PrivateKey',

    #
    #   MingKeMing
    #
    'EntityType', 'MetaType',
    'Address',   # 'AddressFactory',
    'ID',        # 'IDFactory',
    'Meta',      # 'MetaFactory',
    'Document',  # 'DocumentFactory',
    'Visa', 'Bulletin',

    'ANYWHERE', 'EVERYWHERE', 'ANYONE', 'EVERYONE', 'FOUNDER',

    #
    #   DaoKeDao
    #
    'ContentType', 'Content',  # 'ContentFactory',
    'Envelope',                # 'EnvelopeFactory',
    'Message',
    'InstantMessage',          # 'InstantMessageFactory',
    'SecureMessage',           # 'SecureMessageFactory',
    'ReliableMessage',         # 'ReliableMessageFactory',

    # 'InstantMessageDelegate', 'SecureMessageDelegate', 'ReliableMessageDelegate',

    #
    #   DaoKeDao protocol extends
    #
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
]
