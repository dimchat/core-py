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

from mkm import *
from dkd import *

from .protocol import *
from .mkm import *
from .dkd import *

from .barrack import Barrack
from .transceiver import Transceiver
from .packer import Packer
from .processor import Processor

name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [

    #
    #   MingKeMing
    #
    'NetworkType', 'MetaType',
    'Address', 'AddressFactory',
    'ID', 'IDFactory',
    'Meta', 'MetaFactory',
    'Document', 'DocumentFactory',
    'Visa', 'Bulletin',

    'ANYWHERE', 'EVERYWHERE', 'ANYONE', 'EVERYONE', 'FOUNDER',

    'BaseAddressFactory',  # 'BroadcastAddress',
    # 'IdentifierFactory', 'Identifier',
    'BaseMeta',
    'BaseDocument', 'BaseVisa', 'BaseBulletin',

    #
    #   DaoKeDao
    #
    'ContentType', 'Content', 'ContentFactory',
    'Envelope',  # 'EnvelopeFactory',
    'Message', 'InstantMessage', 'SecureMessage', 'ReliableMessage',
    # 'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',
    'InstantMessageDelegate', 'SecureMessageDelegate', 'ReliableMessageDelegate',

    'BaseContent',
    # 'MessageEnvelope', 'MessageEnvelopeFactory',
    # 'BaseMessage',
    # 'PlainMessage', 'PlainMessageFactory',
    # 'EncryptedMessage', 'EncryptedMessageFactory',
    # 'NetworkMessage', 'NetworkMessageFactory',

    #
    #   Protocol
    #
    'TextContent', 'ForwardContent', 'ArrayContent',
    'MoneyContent', 'TransferContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'PageContent', 'CustomizedContent',

    'Command', 'CommandFactory',
    'MetaCommand', 'DocumentCommand',

    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand',
    'QuitCommand', 'QueryCommand', 'ResetCommand',

    #
    #   Core
    #
    'EntityDelegate',
    'EntityDataSource', 'UserDataSource', 'GroupDataSource',
    'Entity', 'User', 'Group',
    'BaseEntity', 'BaseUser', 'BaseGroup',

    'BaseTextContent', 'SecretContent', 'ListContent',
    'BaseMoneyContent', 'TransferMoneyContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'WebPageContent', 'AppCustomizedContent',
    'BaseCommand',
    'BaseMetaCommand', 'BaseDocumentCommand',
    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand',
    'QuitGroupCommand', 'QueryGroupCommand', 'ResetGroupCommand',

    # 'ContentFactoryBuilder', 'CommandFactoryBuilder',
    # 'GeneralCommandFactory', 'HistoryCommandFactory', 'GroupCommandFactory',
    # # register_core_factories
    # 'register_content_factories', 'register_command_factories',

    'Barrack', 'Transceiver', 'Packer', 'Processor',
]
