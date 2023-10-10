# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2023 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2023 Albert Moky
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

from .keys import BaseKey, BaseSymmetricKey
from .keys import BaseAsymmetricKey, BasePublicKey, BasePrivateKey

from .ted import BaseDataWrapper
from .pnf import BaseFileWrapper

__all__ = [

    #
    #   Types
    #
    'URI', 'DateTime',
    'Converter',
    'Wrapper', 'Stringer', 'Mapper',
    'ConstantString',  # 'String',
    'Dictionary',

    #
    #   Data Format
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
    'FormatGeneralFactory', 'FormatFactoryManager',

    #
    #   Data Digest
    #
    'DataDigester',
    'MD5', 'SHA1', 'SHA256', 'KECCAK256', 'RIPEMD160',
    'md5', 'sha1', 'sha256', 'keccak256', 'ripemd160',

    #
    #   Crypto
    #
    'CryptographyKey', 'EncryptKey', 'DecryptKey',
    'AsymmetricKey', 'SignKey', 'VerifyKey',
    'SymmetricKey', 'SymmetricKeyFactory',
    'PublicKey', 'PublicKeyFactory',
    'PrivateKey', 'PrivateKeyFactory',
    'CryptographyKeyGeneralFactory', 'CryptographyKeyFactoryManager',

    #
    #   Base Keys
    #
    'BaseKey', 'BaseSymmetricKey',
    'BaseAsymmetricKey', 'BasePublicKey', 'BasePrivateKey',

    #
    #   TED & PNF
    #
    'BaseDataWrapper',
    'BaseFileWrapper',

]
