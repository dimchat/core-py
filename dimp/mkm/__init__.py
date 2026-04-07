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

from mkm.protocol import *
from mkm.protocol.broadcast import BroadcastAddress, Identifier

from ..protocol import MetaType, DocumentType
from ..protocol import Visa, Bulletin

from .meta import BaseMeta
from .document import BaseDocument
from .docs import BaseVisa, BaseBulletin


__all__ = [

    #
    #   Protocol
    #

    'EntityType',
    'Address', 'ID',
    'Meta', 'TAI', 'Document',

    'AddressFactory', 'IDFactory',
    'MetaFactory', 'DocumentFactory',

    'ANYWHERE', 'EVERYWHERE',
    'ANYONE', 'EVERYONE', 'FOUNDER',
    'BroadcastAddress', 'Identifier',

    # 'AddressHelper', 'IDHelper',
    # 'MetaHelper', 'DocumentHelper',
    # 'AccountExtensions', 'shared_account_extensions',

    #
    #   Extends
    #

    'MetaType', 'DocumentType',
    'Visa', 'Bulletin',

    'BaseMeta',
    'BaseDocument', 'BaseVisa', 'BaseBulletin',

]
