# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
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

from mkm import BroadcastAddress, Identifier

from .format import *
from .crypto import *
from .protocol import *
from .dkd import *
from .ext import *

from .cmd_ext import GeneralCommandHelper, CmdExtension
from .cmd_ext import message_extensions, message_helper, cmd_helper


name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [

    'StrMap', 'MutableStrMap',

    'URI', 'DateTime',

    'Stringer', 'Mapper',

    #
    #   Format
    #

    'DataCoder', 'Hex', 'Base58', 'Base64',
    'ObjectCoder', 'JSON',
    'MapCoder', 'JSONMap',
    'StringCoder', 'UTF8',

    'TransportableResource',
    'TransportableData',

    'TransportableDataFactory',

    'TransportableDataHelper',
    'FormatExtensions', 'shared_format_extensions',

    #
    #   TED
    #

    'BaseString', 'BaseData',

    'PlainData',

    #
    #   PNF
    #

    'TransportableFile', 'TransportableFileFactory',
    'TransportableFileWrapper', 'TransportableFileWrapperFactory',
    'TransportableFileHelper',


    # ================================================================


    #
    #   Digest
    #

    'MessageDigester',
    'SHA256', 'KECCAK256', 'RIPEMD160',

    #
    #   Crypto
    #

    'CryptographyKey',
    'EncryptKey', 'DecryptKey', 'SignKey', 'VerifyKey',
    'SymmetricKey', 'AsymmetricKey',
    'PrivateKey', 'PublicKey',

    'SymmetricKeyFactory', 'PrivateKeyFactory', 'PublicKeyFactory',

    'SymmetricKeyHelper', 'PublicKeyHelper', 'PrivateKeyHelper',

    'SymmetricKeyExtension', 'PublicKeyExtension', 'PrivateKeyExtension',
    'CryptoExtensions', 'shared_crypto_extensions',


    # ================================================================


    #
    #   Ming-Ke-Ming
    #

    'Address', 'ID',
    'Meta', 'Document',

    'BroadcastAddress', 'Identifier',

    'AddressHelper', 'IDHelper',
    'MetaHelper', 'DocumentHelper',

    'AddressExtension', 'IDExtension',
    'MetaExtension', 'DocumentExtension',
    'AccountExtensions', 'shared_account_extensions',

    'CryptoKeyHandler', 'GeneralCryptoExtension',
    'AccountHandler', 'GeneralAccountExtension',

    #
    #   Dao-Ke-Dao
    #

    'Content', 'Envelope',
    'InstantMessage', 'SecureMessage', 'ReliableMessage',

    'ContentFactory', 'EnvelopeFactory',
    'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',

    'ContentHelper', 'EnvelopeHelper',
    'InstantMessageHelper', 'SecureMessageHelper', 'ReliableMessageHelper',

    'ContentExtension',
    'InstantMessageExtension', 'SecureMessageExtension', 'ReliableMessageExtension',
    'MessageExtensions', 'shared_message_extensions',
    'MessageHandler', 'MessageHandlerExtension',

    #
    #   Core Protocols
    #

    'ContentType',

    'Command', 'CommandFactory',
    'CommandHelper', 'GeneralCommandHelper',
    'CommandExtension', 'CmdExtension',

    'message_extensions', 'message_helper', 'cmd_helper',
    'command_helper',

    #
    #   Message Implementations
    #

    'MessageEnvelope',
    'BaseMessage',
    'PlainMessage', 'EncryptedMessage', 'NetworkMessage',

]
