# -*- coding: utf-8 -*-
# ==============================================================================
# MIT License
#
# Copyright (c) 2026 Albert Moky
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

from .duri import Header, DataURI

from .base import EncodeAlgorithms
from .base import BaseString, BaseData

from .data import Base64Data, PlainData
from .embed import EmbedData

from .file import TransportableFile, TransportableFileFactory
# from .file import TransportableFileHelper
from .file_wrapper import TransportableFileWrapper, TransportableFileWrapperFactory
from .pnf import PortableNetworkFile
from .pnf_wrapper import PortableNetworkFileWrapper


__all__ = [

    'Header', 'DataURI',

    #
    #   TransportableData
    #

    'EncodeAlgorithms',

    'BaseString', 'BaseData',

    'Base64Data', 'PlainData',
    'EmbedData',

    #
    #   TransportableFile
    #

    'TransportableFile', 'TransportableFileFactory',
    # 'TransportableFileHelper',
    'TransportableFileWrapper', 'TransportableFileWrapperFactory',

    'PortableNetworkFile', 'PortableNetworkFileWrapper',

]
