# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2025 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2025 Albert Moky
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


class AsymmetricAlgorithms:
    """ Algorithms for Asymmetric Key """

    RSA = 'RSA'  # -- "RSA/ECB/PKCS1Padding", "SHA256withRSA"
    ECC = 'ECC'


class SymmetricAlgorithms:
    """ Algorithms for Symmetric Key """

    AES = 'AES'  # -- "AES/CBC/PKCS7Padding"
    DES = 'DES'

    # Symmetric key algorithm for broadcast message,
    # which will do nothing when en/decoding message data
    PLAIN = 'PLAIN'


class EncodeAlgorithms:
    """ Algorithms for Encoding Data """

    DEFAULT = 'base64'

    BASE_64 = 'base64'
    BASE_58 = 'base58'
    HEX = 'hex'
