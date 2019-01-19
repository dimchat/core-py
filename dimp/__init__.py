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
from mkm import NetworkID, Address, ID, Meta, Entity
from mkm import Account, User, Group

from dkd import MessageType, Content
from dkd import TextContent, CommandContent, ForwardContent
from dkd import Envelope, Message
from dkd import InstantMessage, SecureMessage, ReliableMessage

from dimp.commands import handshake_start_command, handshake_again_command, handshake_success_command
from dimp.commands import invite_command, expel_command, quit_command
from dimp.commands import broadcast_command

name = "DIMP"

__author__ = 'Albert Moky'

__all__ = [
    # Crypto
    'SymmetricKey',
    'PrivateKey', 'PublicKey',

    # MingKeMing
    'NetworkID', 'Address', 'ID', 'Meta',
    'Entity',
    'Account', 'User',
    'Group',

    # DaoKeDao
    'MessageType', 'Content',
    'TextContent', 'CommandContent', 'ForwardContent',
    'Envelope', 'Message',
    'InstantMessage', 'SecureMessage', 'ReliableMessage',

    # DIMP
    'handshake_start_command', 'handshake_again_command', 'handshake_success_command',
    'invite_command', 'expel_command', 'quit_command',
    'broadcast_command',
]
