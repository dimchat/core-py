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

    Decentralized Instant Message Plugins
"""

from mkm.ext import *
from dkd.ext import *

from ..format.pnf import TransportableFileHelper
from ..format.pnf import TransportableFileExtension
# from ..format.pnf import format_extensions
from ..format.pnf import pnf_helper

from ..format.pnf_wrapper import TransportableFileWrapperExtension
from ..format.pnf_wrapper import wrapper_factory

from ..protocol.command import CommandHelper, CommandExtension

from .cmd_ext import CommandHandler, GeneralCommandExtension
# from .cmd_ext import command_extensions
from .cmd_ext import command_handler


__all__ = [

    #
    #   Format
    #

    'TransportableDataHelper',
    'FormatExtensions', 'shared_format_extensions',

    #
    #   Crypto
    #

    'SymmetricKeyHelper', 'PublicKeyHelper', 'PrivateKeyHelper',

    'SymmetricKeyExtension', 'PublicKeyExtension', 'PrivateKeyExtension',
    'CryptoExtensions', 'shared_crypto_extensions',


    'EncryptedBundleHandler', 'DefaultBundleHandler',
    'EncryptedBundleExtension',


    #
    #   Ming-Ke-Ming
    #

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

    'ContentHelper', 'EnvelopeHelper',
    'InstantMessageHelper', 'SecureMessageHelper', 'ReliableMessageHelper',

    'ContentExtension',
    'InstantMessageExtension', 'SecureMessageExtension', 'ReliableMessageExtension',
    'MessageExtensions', 'shared_message_extensions',

    'MessageHandler', 'MessageHandlerExtension',

    # ----------------------------------------------------------------

    #
    #   Format
    #

    'TransportableFileHelper',
    'TransportableFileExtension',
    'TransportableFileWrapperExtension',

    # 'format_extensions',
    'pnf_helper',
    'wrapper_factory',

    #
    #   Command
    #

    'CommandHelper', 'CommandHandler',
    'CommandExtension', 'GeneralCommandExtension',

    # 'command_extensions',
    'command_handler',

]
