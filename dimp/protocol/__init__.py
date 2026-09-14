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

from mkm.protocol import *
from dkd.protocol import *

from .types import ContentType

from .command import Command, CommandFactory
# from .command import CommandHelper
# from .command import CommandExtension


__all__ = [

    #
    #   Ming-Ke-Ming
    #

    'EntityType',
    'Address', 'ID',
    'Meta', 'TAI', 'Document',

    'AddressFactory', 'IDFactory',
    'MetaFactory', 'DocumentFactory',

    'ANYWHERE', 'EVERYWHERE',
    'ANYONE', 'EVERYONE', 'FOUNDER',
    # 'BroadcastAddress', 'Identifier',

    # 'AddressHelper', 'IDHelper',
    # 'MetaHelper', 'DocumentHelper',

    # 'AddressExtension', 'IDExtension',
    # 'MetaExtension', 'DocumentExtension',
    # 'AccountExtensions', 'shared_account_extensions',


    #
    #   Dao-Ke-Dao
    #

    'Content', 'Envelope',
    'Message',
    'InstantMessage', 'SecureMessage', 'ReliableMessage',

    'ContentFactory', 'EnvelopeFactory',
    'InstantMessageFactory', 'SecureMessageFactory', 'ReliableMessageFactory',

    # 'ContentHelper', 'EnvelopeHelper',
    # 'InstantMessageHelper', 'SecureMessageHelper', 'ReliableMessageHelper',

    # 'ContentExtension',
    # 'InstantMessageExtension', 'SecureMessageExtension', 'ReliableMessageExtension',
    # 'MessageExtensions', 'shared_message_extensions',

    #
    #   Protocol
    #

    'ContentType',

    'Command', 'CommandFactory',
    # 'CommandHelper',
    # 'CommandExtension',

]
