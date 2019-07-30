# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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

from mkm import SymmetricKey, PrivateKey, PublicKey
from mkm import NetworkID, Address, ID, Meta, Profile
from mkm import Entity, IEntityDataSource
from mkm import Account, User, IUserDataSource
from mkm import Group, IGroupDataSource

from dkd import Content
from dkd import Envelope, Message
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import IInstantMessageDelegate, ISecureMessageDelegate, IReliableMessageDelegate

from .protocol import ContentType, TextContent, CommandContent, HistoryContent, ForwardContent
from .commands import HandshakeCommand, MetaCommand, ProfileCommand, ReceiptCommand, GroupCommand

from .delegate import ICallback, ICompletionHandler, ITransceiverDelegate
from .barrack import Barrack
from .keystore import KeyCache
from .transceiver import Transceiver

from .station import ServiceProvider, Station
from .certificate import CASubject, CAValidity, CAData, CertificateAuthority

name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [
    # Crypto
    'SymmetricKey',
    'PrivateKey', 'PublicKey',

    # MingKeMing
    'NetworkID', 'Address', 'ID', 'Meta', 'Profile',
    'Entity', 'IEntityDataSource',
    'Account', 'User', 'IUserDataSource',
    'Group', 'IGroupDataSource',

    # DaoKeDao
    'Content',
    'Envelope', 'Message',
    # message transform
    'InstantMessage', 'SecureMessage', 'ReliableMessage',
    'IInstantMessageDelegate', 'ISecureMessageDelegate', 'IReliableMessageDelegate',

    # DIMP
    'ContentType',
    'TextContent', 'CommandContent', 'HistoryContent', 'ForwardContent',
    'HandshakeCommand', 'MetaCommand', 'ProfileCommand', 'ReceiptCommand',
    'GroupCommand',

    'ICallback', 'ICompletionHandler', 'ITransceiverDelegate',
    'Barrack',
    'KeyCache',
    'Transceiver',

    'ServiceProvider', 'Station',
    'CASubject', 'CAValidity', 'CAData', 'CertificateAuthority',
]
