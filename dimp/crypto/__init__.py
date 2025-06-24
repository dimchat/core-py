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

from mkm.crypto import *

from .algorithms import AsymmetricAlgorithms, SymmetricAlgorithms
from .algorithms import EncodeAlgorithms

from .keys import BaseKey, BaseSymmetricKey
from .keys import BaseAsymmetricKey, BasePublicKey, BasePrivateKey

from .ted import BaseDataWrapper
from .pnf import BaseFileWrapper

__all__ = [

    #
    #   Data Digest
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

    #
    #   Algorithm
    #
    'AsymmetricAlgorithms', 'SymmetricAlgorithms',
    'EncodeAlgorithms',

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
