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

from mkm.protocol import *
from dkd.protocol import *

from .types import ContentType

from .command import Command, CommandFactory
# from .command import CommandExtension
# from .command import CommandHelper
# from .command import command_helper


__all__ = [

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
    #   Core Protocol
    #

    'ContentType',

    'Command', 'CommandFactory',
    # 'CommandExtension',
    # 'CommandHelper',
    # 'command_helper',

]
