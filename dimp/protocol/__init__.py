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

"""
    DIMP - Message Contents & Commands
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Define universal message types as contents and commands
"""

from mkm import ID, SymmetricKey
import dkd

from .content import Content
from .forward import ForwardContent
from .text import TextContent
from .file import FileContent, ImageContent, AudioContent, VideoContent

from .command import Command
from .history import HistoryCommand

from .group import GroupCommand
from .group import InviteCommand, ExpelCommand, JoinCommand, QuitCommand
from .group import QueryCommand, ResetCommand

from .meta import MetaCommand
from .profile import ProfileCommand

#
#  Conveniences for Generic
#
Envelope = dkd.Envelope[ID]
Message = dkd.Message[ID, SymmetricKey]
InstantMessage = dkd.InstantMessage[ID, SymmetricKey]
SecureMessage = dkd.SecureMessage[ID, SymmetricKey]
ReliableMessage = dkd.ReliableMessage[ID, SymmetricKey]
# Delegates
InstantMessageDelegate = dkd.InstantMessageDelegate[ID, SymmetricKey]
SecureMessageDelegate = dkd.SecureMessageDelegate[ID, SymmetricKey]
ReliableMessageDelegate = dkd.ReliableMessageDelegate[ID, SymmetricKey]


__all__ = [
    'Envelope', 'Message', 'InstantMessage', 'SecureMessage', 'ReliableMessage',
    'InstantMessageDelegate', 'SecureMessageDelegate', 'ReliableMessageDelegate',

    'Content', 'ForwardContent', 'TextContent',
    'FileContent', 'ImageContent', 'AudioContent', 'VideoContent',

    'Command', 'HistoryCommand', 'GroupCommand',
    'InviteCommand', 'ExpelCommand', 'JoinCommand', 'QuitCommand',
    'QueryCommand', 'ResetCommand',

    'MetaCommand', 'ProfileCommand',
]
