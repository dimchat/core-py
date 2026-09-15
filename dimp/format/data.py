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

from mkm.types import final
from mkm.format import UTF8

from .base import BaseData


@final
class PlainData(BaseData):
    """ UTF-8 encoding """

    @property
    def encoding(self) -> str:
        return ''  # no encoding, 'PLAIN'

    # Override
    def to_bytes(self) -> Optional[bytes]:
        data = self._binary
        if data is None:
            txt = self._string
            assert txt is not None, f'PlainData error: {self}'
            data = UTF8.encode(string=txt)
            self._binary = data
        return data

    # Override
    def to_str(self) -> str:
        txt = self._string
        if txt is None or len(txt) == 0:
            data = self._binary
            if data is None:
                assert False, f'PlainData error: {self}'
            else:
                txt = UTF8.decode(data=data)
                self._string = txt
            assert txt is not None and len(txt) > 0, f'PlainData error: {data}'
        return txt

    #
    #   Factories
    #

    @classmethod
    def new(cls, string: str, binary: bytes):
        """ Create with encoded string and decoded bytes. """
        return PlainData(string=string, binary=binary)

    @classmethod
    def create_with_string(cls, string: str):
        """ Create with encoded string only (decode lazily). """
        return PlainData(string=string, binary=None)

    @classmethod
    def create_with_bytes(cls, binary: bytes):
        """ Create with decoded bytes only (encode lazily). """
        return PlainData(string='', binary=binary)

    @classmethod
    def zero(cls):
        """ empty data """
        return PlainData(string='', binary=b'')
