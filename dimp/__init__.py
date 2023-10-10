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

from mkm.types import *
from mkm.format import *
from mkm.crypto import *
from mkm import *
from dkd import *

from .crypto import *
from .protocol import *
from .mkm import *
from .dkd import *
from .msg import *

from .barrack import Barrack
from .transceiver import Transceiver
from .packer import Packer
from .processor import Processor

name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [

    #
    #   Types
    #

    'URI', 'DateTime',
    # 'Converter',
    # 'Wrapper', 'Stringer', 'Mapper',
    # 'ConstantString',  # 'String',
    # 'Dictionary',

    #
    #   Format
    #

    # 'DataCoder', 'Hex', 'Base64', 'Base58',
    # 'ObjectCoder', 'JSON',
    # 'MapCoder', 'JSONMap',
    # 'ListCoder', 'JSONList',
    # 'StringCoder', 'UTF8',

    'hex_encode', 'hex_decode',
    'base64_encode', 'base64_decode', 'base58_encode', 'base58_decode',
    'json_encode', 'json_decode',
    'utf8_encode', 'utf8_decode',

    'TransportableData',
    'PortableNetworkFile',
    # 'TransportableDataFactory',
    # 'PortableNetworkFileFactory',
    # 'FormatGeneralFactory',
    # 'FormatFactoryManager',

    #
    #   Crypto
    #

    # 'DataDigester',
    # 'MD5', 'SHA1', 'SHA256', 'KECCAK256', 'RIPEMD160',

    'md5', 'sha1', 'sha256', 'keccak256', 'ripemd160',

    # 'CryptographyKey',
    'SymmetricKey', 'EncryptKey', 'DecryptKey',
    'AsymmetricKey', 'SignKey', 'VerifyKey',
    'PublicKey', 'PrivateKey',
    # 'SymmetricKeyFactory',
    # 'PublicKeyFactory', 'PrivateKeyFactory',

    # 'BaseKey', 'BaseSymmetricKey',
    # 'BaseAsymmetricKey', 'BasePublicKey', 'BasePrivateKey',
    # 'BaseDataWrapper', 'BaseFileWrapper',

    #
    #   MingKeMing
    #

    'EntityType', 'MetaType',
    'Address', 'ID', 'Meta',
    'Document', 'Visa', 'Bulletin',

    # 'AddressFactory', 'IDFactory',
    # 'MetaFactory',
    # 'DocumentFactory',

    # 'BroadcastAddress', 'Identifier',
    # 'AccountGeneralFactory', 'AccountFactoryManager',
    'ANYWHERE', 'EVERYWHERE', 'ANYONE', 'EVERYONE', 'FOUNDER',

    # 'BaseMeta', 'MetaHelper',
    # 'BaseDocument', 'BaseVisa', 'BaseBulletin',

    'EntityDelegate',
    'EntityDataSource', 'UserDataSource', 'GroupDataSource',
    'Entity', 'User', 'Group',
    # 'BaseEntity', 'BaseUser', 'BaseGroup',

    #
    #   DaoKeDao
    #

    'ContentType', 'Content', 'Envelope',
    'Message', 'InstantMessage', 'SecureMessage', 'ReliableMessage',
    # 'ContentFactory', 'EnvelopeFactory',
    # 'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',
    # 'InstantMessageDelegate', 'SecureMessageDelegate', 'ReliableMessageDelegate',
    # 'MessageGeneralFactory', 'MessageFactoryManager',

    'TextContent', 'ArrayContent', 'ForwardContent',
    'PageContent', 'NameCard',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'MoneyContent', 'TransferContent',
    'CustomizedContent',

    'Command',  # 'CommandFactory',
    'MetaCommand', 'DocumentCommand',
    'ReceiptCommand',   # 'ReceiptCommandMixIn',

    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'QueryCommand', 'ResetCommand',
    'HireCommand', 'FireCommand', 'ResignCommand',

    # 'BaseContent',
    # 'BaseTextContent', 'ListContent', 'SecretContent',
    # 'WebPageContent', 'NameCardContent',
    # 'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    # 'BaseMoneyContent', 'TransferMoneyContent',
    # 'AppCustomizedContent',
    #
    # 'BaseCommand',
    # 'BaseMetaCommand', 'BaseDocumentCommand',
    # 'BaseReceipt', 'BaseReceiptCommand',
    #
    # 'BaseHistoryCommand', 'BaseGroupCommand',
    # 'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand',
    # 'QuitGroupCommand', 'QueryGroupCommand', 'ResetGroupCommand',
    # 'HireGroupCommand', 'FireGroupCommand', 'ResignGroupCommand',

    # 'MessageEnvelope', 'BaseMessage',
    # 'PlainMessage', 'EncryptedMessage', 'NetworkMessage',

    #
    #   Core
    #
    'Barrack', 'Transceiver', 'Packer', 'Processor',
]
