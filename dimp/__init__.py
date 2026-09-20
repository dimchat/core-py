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

"""
    DIMP
    ~~~~

    Decentralized Instant Messaging Protocol
"""

from .types import *
from .format import *
from .crypto import *
from .protocol import *
from .dkd import *
from .ext import *


name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [

    'Singleton',

    'final',

    'StrMap', 'MutableStrMap',
    'AnyList', 'StrList',

    'URI', 'DateTime',

    'Stringer',
    'ConstantString',  # 'String',
    'Mapper',

    'Converter', 'DataConverter', 'BaseConverter',
    'Copier', 'DataCopier', 'BaseCopier',
    'Wrapper', 'DataWrapper', 'BaseWrapper',

    'Dictionary',

    ################################################################
    #
    #   Format
    #
    ################################################################

    'DataCoder', 'Hex', 'Base58', 'Base64',

    'ObjectCoder', 'JSON',
    'MapCoder', 'JSONMap',
    'StringCoder', 'UTF8',

    'TransportableResource',
    'TransportableData', 'TransportableDataFactory',
    # 'FormatExtensions',
    # 'TransportableDataHelper',
    # 'shared_format_extensions', 'ted_helper',

    #
    #   TED
    #

    'BaseString', 'BaseData',

    'PlainData',

    #
    #   PNF
    #

    'TransportableFile', 'TransportableFileFactory',
    # 'TransportableFileExtension',
    # 'TransportableFileHelper',
    # 'pnf_helper',
    'TransportableFileWrapper', 'TransportableFileWrapperFactory',
    # 'TransportableFileWrapperExtension',
    # 'pnf_wrapper_factory',

    ################################################################
    #
    #   Crypto
    #
    ################################################################

    'MessageDigester',
    'SHA256', 'KECCAK256', 'RIPEMD160',

    #
    #   Crypto
    #

    'CryptographyKey', 'EncryptKey', 'DecryptKey',
    'AsymmetricKey', 'SignKey', 'VerifyKey',
    # 'CryptoExtensions',
    # 'shared_crypto_extensions',

    'SymmetricKey', 'SymmetricKeyFactory',
    # 'SymmetricKeyExtension',
    # 'SymmetricKeyHelper',
    # 'symmetric_helper',

    'PublicKey', 'PublicKeyFactory',
    # 'PublicKeyExtension',
    # 'PublicKeyHelper',
    # 'public_helper',

    'PrivateKey', 'PrivateKeyFactory',
    # 'PrivateKeyExtension',
    # 'PrivateKeyHelper',
    # 'private_helper',

    #
    #   Encrypted Key Bundle
    #

    'BytesMap',

    'EncryptedBundle',
    # 'EncryptedBundleExtension',
    # 'EncryptedBundleHandler',
    # 'bundle_handler',

    'UserEncryptedBundle',

    # 'DefaultBundleHandler',

    ################################################################
    #
    #   Protocol
    #
    ################################################################

    #
    #   Ming-Ke-Ming
    #

    'EntityType',
    # 'AccountExtensions',
    # 'shared_account_extensions',

    'Address', 'AddressFactory',
    # 'AddressExtension',
    # 'AddressHelper',
    # 'address_helper',

    'ID', 'IDFactory',
    # 'IDExtension',
    # 'IDHelper',
    # 'id_helper',

    'Meta', 'MetaFactory',
    # 'MetaExtension',
    # 'MetaHelper',
    # 'meta_helper',

    'TAI',
    'Document', 'DocumentFactory',
    # 'DocumentExtension',
    # 'DocumentHelper',
    # 'doc_helper',

    'ANYWHERE', 'EVERYWHERE',
    'ANYONE', 'EVERYONE', 'FOUNDER',
    'Identifier',  # 'BroadcastAddress',

    #
    #   Dao-Ke-Dao
    #

    'Message',
    # 'MessageExtensions',
    # 'shared_message_extensions',

    'Envelope', 'EnvelopeFactory',
    # 'EnvelopeHelper',
    # 'envelope_helper',

    'InstantMessage', 'InstantMessageFactory',
    # 'InstantMessageExtension',
    # 'InstantMessageHelper',
    # 'instant_helper',

    'SecureMessage', 'SecureMessageFactory',
    # 'SecureMessageExtension',
    # 'SecureMessageHelper',
    # 'secure_helper',

    'ReliableMessage', 'ReliableMessageFactory',
    # 'ReliableMessageExtension',
    # 'ReliableMessageHelper',
    # 'reliable_helper',

    'Content', 'ContentFactory',
    # 'ContentExtension',
    # 'ContentHelper',
    # 'content_helper',

    #
    #   Core Protocols
    #

    'ContentType',

    'Command', 'CommandFactory',
    # 'CommandExtension',
    # 'CommandHelper',
    # 'command_helper',

    #
    #   Message Implementations
    #

    'MessageEnvelope',

    'BaseMessage',
    'PlainMessage',
    'EncryptedMessage',
    'NetworkMessage',

    ################################################################
    #
    #   Extensions
    #
    ################################################################

    #
    #   Format
    #

    'FormatExtensions',
    'TransportableDataHelper',
    'shared_format_extensions', 'ted_helper',

    #
    #   Crypto
    #

    'CryptoExtensions',
    'shared_crypto_extensions',

    'SymmetricKeyExtension',
    'SymmetricKeyHelper',
    'symmetric_helper',

    'PublicKeyExtension',
    'PublicKeyHelper',
    'public_helper',

    'PrivateKeyExtension',
    'PrivateKeyHelper',
    'private_helper',

    #
    #   Account
    #

    'AccountExtensions',
    'shared_account_extensions',

    'AddressExtension',
    'AddressHelper',
    'address_helper',

    'IDExtension',
    'IDHelper',
    'id_helper',

    'MetaExtension',
    'MetaHelper',
    'meta_helper',

    'DocumentExtension',
    'DocumentHelper',
    'doc_helper',

    #
    #   General Extensions
    #

    'GeneralCryptoExtension',
    'CryptoKeyHandler',
    'crypto_handler',

    'GeneralAccountExtension',
    'AccountHandler',
    'account_handler',

    #
    #   Bundle
    #

    'EncryptedBundleExtension',
    'EncryptedBundleHandler',
    'bundle_handler',

    'DefaultBundleHandler',

    #
    #   Message
    #

    'MessageExtensions',
    'shared_message_extensions',

    'EnvelopeHelper',
    'envelope_helper',

    'InstantMessageExtension',
    'InstantMessageHelper',
    'instant_helper',

    'SecureMessageExtension',
    'SecureMessageHelper',
    'secure_helper',

    'ReliableMessageExtension',
    'ReliableMessageHelper',
    'reliable_helper',

    'ContentExtension',
    'ContentHelper',
    'content_helper',

    #
    #   General Extensions
    #

    'MessageHandlerExtension',
    'MessageHandler',
    'message_handler',

    #
    #   Transportable File
    #

    'TransportableFileExtension',
    'TransportableFileHelper',
    'pnf_helper',

    'TransportableFileWrapperExtension',
    'pnf_wrapper_factory',

    #
    #   Command
    #

    'CommandExtension',
    'CommandHelper',
    'command_helper',

    'GeneralCommandExtension',
    'CommandHandler',
    'command_handler',

]
