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

from ..format.pnf import TransportableFileExtension
from ..format.pnf import TransportableFileHelper
from ..format.pnf import pnf_helper

from ..format.pnf_wrapper import TransportableFileWrapperExtension
from ..format.pnf_wrapper import pnf_wrapper_factory

from ..protocol.command import CommandExtension
from ..protocol.command import CommandHelper
from ..protocol.command import command_helper

from .cmd_ext import GeneralCommandExtension
from .cmd_ext import CommandHandler
from .cmd_ext import command_handler


__all__ = [

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
