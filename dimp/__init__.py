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

from .protocol.commands import CommandFactory
from .protocol import *
from .crypto import *
from .mkm import *
from .dkd import *
from .msg import *


name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [

    'Singleton',

    'URI', 'DateTime',

    'Converter', 'Copier',
    'Wrapper', 'Stringer', 'Mapper',
    'ConstantString',  # 'String',
    'Dictionary',

    #
    #   Format
    #

    'DataCoder', 'Hex', 'Base58', 'Base64',
    'ObjectCoder', 'JSON',
    'MapCoder', 'JSONMap',
    'ListCoder', 'JSONList',
    'StringCoder', 'UTF8',

    'hex_encode', 'hex_decode',
    'base58_encode', 'base58_decode',
    'base64_encode', 'base64_decode',
    'json_encode', 'json_decode',
    'utf8_encode', 'utf8_decode',

    'TransportableData', 'TransportableDataFactory',
    'PortableNetworkFile', 'PortableNetworkFileFactory',

    #
    #   Digest
    #

    'DataDigester',
    'MD5', 'SHA1', 'SHA256', 'KECCAK256', 'RIPEMD160',

    'md5', 'sha1', 'sha256', 'keccak256', 'ripemd160',

    #
    #   Crypto
    #

    'CryptographyKey',
    'EncryptKey', 'DecryptKey', 'SignKey', 'VerifyKey',
    'SymmetricKey', 'AsymmetricKey',
    'PrivateKey', 'PublicKey',

    'SymmetricKeyFactory', 'PrivateKeyFactory', 'PublicKeyFactory',

    'BaseKey', 'BaseSymmetricKey',
    'BaseAsymmetricKey', 'BasePublicKey', 'BasePrivateKey',

    'BaseDataWrapper',
    'BaseFileWrapper',

    #
    #   Algorithm
    #
    'AsymmetricAlgorithms', 'SymmetricAlgorithms',
    'EncodeAlgorithms',

    #
    #   MingKeMing
    #

    'EntityType',
    'Address',
    'ID',
    'Meta',
    'Document', 'Visa', 'Bulletin',

    'AddressFactory',
    'IDFactory',
    'MetaFactory',
    'DocumentFactory',

    'Identifier',
    'ANYONE', 'EVERYONE', 'FOUNDER',
    'ANYWHERE', 'EVERYWHERE',
    # 'BroadcastAddress',

    'BaseMeta',
    'BaseDocument', 'BaseVisa', 'BaseBulletin',

    'MetaType', 'DocumentType',

    #
    #   DaoKeDao
    #

    'ContentType',
    'Content',
    'Envelope',
    'Message',
    'InstantMessage', 'SecureMessage', 'ReliableMessage',

    # contents
    'TextContent', 'ArrayContent', 'ForwardContent',
    'PageContent', 'NameCard',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',
    'MoneyContent', 'TransferContent',
    'QuoteContent', 'CombineContent',

    # commands
    'Command',
    'MetaCommand', 'DocumentCommand',
    'ReceiptCommand',

    # group history
    'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand', 'QueryCommand', 'ResetCommand',
    'HireCommand', 'FireCommand', 'ResignCommand',

    # extend contents
    'BaseContent',
    'BaseTextContent', 'ListContent', 'SecretContent',
    'WebPageContent', 'NameCardContent',
    'BaseFileContent', 'ImageFileContent', 'AudioFileContent', 'VideoFileContent',
    'BaseMoneyContent', 'TransferMoneyContent',
    'BaseQuoteContent', 'CombineForwardContent',

    # extend commands
    'BaseCommand',
    'BaseMetaCommand', 'BaseDocumentCommand',
    'BaseReceiptCommand',

    # extend group history
    'BaseHistoryCommand', 'BaseGroupCommand',
    'InviteGroupCommand', 'ExpelGroupCommand', 'JoinGroupCommand',
    'QuitGroupCommand', 'QueryGroupCommand', 'ResetGroupCommand',
    'HireGroupCommand', 'FireGroupCommand', 'ResignGroupCommand',

    #
    #   Message
    #

    'MessageEnvelope',
    'BaseMessage',
    'PlainMessage', 'EncryptedMessage', 'NetworkMessage',

    # factories
    'ContentFactory', 'CommandFactory',
    'EnvelopeFactory',
    'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',

]
