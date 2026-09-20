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

"""
    Cryptography
    ~~~~~~~~~~~~

    1. Crypto Keys
    2. Data Digest
    3. Data Format
"""

from mkm.digest import *
from mkm.crypto import *
from dkd.crypto import *


__all__ = [

    #
    #   Digest
    #

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

]
