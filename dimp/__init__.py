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
from mkm import NetworkID, Address, ID, Meta
from mkm import Entity, IEntityDataSource
from mkm import Account, User, IAccountDelegate, IUserDelegate, IUserDataSource
from mkm import Group, IGroupDelegate, IGroupDataSource

from dkd import MessageType, Content
from dkd import TextContent, CommandContent, HistoryContent, ForwardContent
from dkd import Envelope, Message, IMessageDelegate
from dkd import InstantMessage, SecureMessage, ReliableMessage
from dkd import IInstantMessageDelegate, ISecureMessageDelegate, IReliableMessageDelegate

from .certificate import CASubject, CAValidity, CAData, CertificateAuthority
from .station import ServiceProvider, Station
from .barrack import Barrack
from .keystore import KeyStore
from .transceiver import Transceiver
from .commands import HandshakeCommand, MetaCommand, ProfileCommand
from .commands import BroadcastCommand, GroupCommand

name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [
    # Crypto
    'SymmetricKey',
    'PrivateKey', 'PublicKey',

    # MingKeMing
    'NetworkID', 'Address', 'ID', 'Meta',
    'Entity', 'IEntityDataSource',
    'Account', 'User', 'IAccountDelegate', 'IUserDelegate', 'IUserDataSource',
    'Group', 'IGroupDelegate', 'IGroupDataSource',

    # DaoKeDao
    'MessageType', 'Content',
    'TextContent', 'CommandContent', 'HistoryContent', 'ForwardContent',
    'Envelope', 'Message', 'IMessageDelegate',
    # message transform
    'InstantMessage', 'SecureMessage', 'ReliableMessage',
    'IInstantMessageDelegate', 'ISecureMessageDelegate', 'IReliableMessageDelegate',

    # DIMP
    'CASubject', 'CAValidity', 'CAData', 'CertificateAuthority',
    'ServiceProvider', 'Station',
    'Barrack', 'KeyStore', 'Transceiver',
    'HandshakeCommand', 'MetaCommand', 'ProfileCommand',
    'BroadcastCommand', 'GroupCommand',
]
