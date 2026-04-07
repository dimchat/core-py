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

from typing import Optional

from mkm.format import base64_encode, base64_decode
from mkm.format import utf8_encode, utf8_decode

from .base import EncodeAlgorithms
from .base import BaseData


class Base64Data(BaseData):
    """ Base-64 encoding """

    @property
    def encoding(self) -> str:
        return EncodeAlgorithms.BASE_64

    @property
    def binary(self) -> Optional[bytes]:
        data = self._binary
        if data is None:
            base64 = self._string
            assert base64 is not None, 'Base64Data error: %s' % self
            data = base64_decode(string=base64)
            self._binary = data
        return data

    @property
    def string(self) -> str:
        base64 = self._string
        if base64 is None or len(base64) == 0:
            data = self._binary
            assert data is not None, 'Base64Data error: %s' % self
            base64 = base64_encode(data=data)
            self._string = base64
        return base64

    #
    #   Factory
    #

    @classmethod
    def create(cls, string: str = None, binary: bytes = None):
        assert not (string is None and binary is None), \
            'encoded string and binary data should not be empty at the same time'
        return Base64Data(string=string, binary=binary)


class PlainData(BaseData):
    """ UTF-8 encoding """

    @property
    def encoding(self) -> str:
        return ''  # 'PLAIN'

    @property
    def binary(self) -> Optional[bytes]:
        data = self._binary
        if data is None:
            txt = self._string
            assert txt is not None, 'PlainData error: %s' % self
            data = utf8_encode(string=txt)
            self._binary = data
        return data

    @property
    def string(self) -> str:
        txt = self._string
        if txt is None or len(txt) == 0:
            data = self._binary
            assert data is not None, 'PlainData error: %s' % self
            txt = utf8_decode(data=data)
            self._string = txt
        return txt

    #
    #   Factories
    #

    @classmethod
    def create(cls, string: str = None, binary: bytes = None):
        assert not (string is None and binary is None), \
            'text string and binary data should not be empty at the same time'
        return PlainData(string=string, binary=binary)

    @classmethod
    def zero(cls):
        """ empty data """
        return PlainData(string='', binary=b'')
