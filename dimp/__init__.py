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

from mkm.crypto import *
from mkm import *
from dkd import *

from .protocol import *

from .entity import Entity, EntityDataSource
from .user import User, UserDataSource
from .group import Group, GroupDataSource

from .delegate import EntityDelegate, CipherKeyDelegate

from .barrack import Barrack
from .transceiver import Transceiver
from .packer import Packer
from .processor import Processor

name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [

    #
    #   Crypto
    #
    'DataCoder', 'Base64', 'Base58', 'Hex',
    'base64_encode', 'base64_decode', 'base58_encode', 'base58_decode', 'hex_encode', 'hex_decode',
    'DataParser', 'JSON', 'UTF8',
    'json_encode', 'json_decode', 'utf8_encode', 'utf8_decode',

    'DataDigester', 'MD5', 'SHA1', 'SHA256', 'KECCAK256', 'RIPEMD160',
    'md5', 'sha1', 'sha256', 'keccak256', 'ripemd160',

    'Wrapper', 'Array', 'Map', 'Dictionary', 'String',

    'CryptographyKey',
    'SymmetricKey', 'EncryptKey', 'DecryptKey',
    'AsymmetricKey', 'SignKey', 'VerifyKey',
    'PublicKey', 'PrivateKey',

    #
    #   MingKeMing
    #
    'NetworkType', 'MetaType',
    'Address', 'AddressFactory', 'ANYWHERE', 'EVERYWHERE',
    'ID', 'ANYONE', 'EVERYONE', 'FOUNDER',
    'Meta', 'BaseMeta',
    'Document', 'BaseDocument',
    'Visa', 'BaseVisa', 'Bulletin', 'BaseBulletin',

    #
    #   DaoKeDao
    #
    'ContentType',
    'Content', 'BaseContent',
    'Envelope',
    'Message',
    'InstantMessage', 'SecureMessage', 'ReliableMessage',
    'MessageDelegate',
    'InstantMessageDelegate', 'SecureMessageDelegate', 'ReliableMessageDelegate',

    #
    #   Protocol
    #
    'ForwardContent', 'TextContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',

    'Command', 'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand',
    'QueryCommand', 'ResetCommand',

    'MetaCommand', 'DocumentCommand',

    #
    #   Core
    #
    'Entity', 'User', 'Group',
    'EntityDataSource', 'UserDataSource', 'GroupDataSource',

    'EntityDelegate', 'CipherKeyDelegate',
    'Barrack', 'Transceiver', 'Packer', 'Processor',
]
