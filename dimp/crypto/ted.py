# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2023 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2023 Albert Moky
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

from typing import Optional, Any, Dict

from mkm.format import base64_encode, base64_decode
from mkm.format import base58_encode, base58_decode
from mkm.format import hex_encode, hex_decode
from mkm.format import TransportableData
from mkm.types import Dictionary


class BaseDataWrapper(Dictionary):
    """
        Transportable Data Mixin

            {
                algorithm : "base64",
                data      : "...",      // base64_encode(data)
                ...
            }

        data format:
            0. "{BASE64_ENCODE}"
            1. "base64,{BASE64_ENCODE}"
            2. "data:image/png;base64,{BASE64_ENCODE}"
    """

    def __init__(self, dictionary: Dict[str, Any]):
        super().__init__(dictionary=dictionary)
        # binary data
        self.__data: Optional[bytes] = None

    # Override
    def __str__(self) -> str:
        text = self.get_str(key='data', default='')
        if len(text) == 0:
            return text
        alg = self.get_str(key='algorithm', default='')
        if alg == TransportableData.DEFAULT:
            alg = ''
        if len(alg) == 0:
            # 0. "{BASE64_ENCODE}"
            return text
        else:
            # 1. "base64,{BASE64_ENCODE}"
            return '%s,%s' % (alg, text)

    def encode(self, mime_type: str) -> str:
        """ toString(mimeType) """
        # get encoded data
        text = self.get_str(key='data', default='')
        if len(text) == 0:
            return text
        alg = self.algorithm
        # 2. "data:image/png;base64,{BASE64_ENCODE}"
        return 'data:%s;%s,%s' % (mime_type, alg, text)

    #
    #   encode algorithm
    #

    @property
    def algorithm(self) -> str:
        alg = self.get_str(key='algorithm', default='')
        if len(alg) == 0:
            alg = TransportableData.DEFAULT
        return alg

    @algorithm.setter
    def algorithm(self, name: str):
        if name is None:  # or name == TransportableData.DEFAULT:
            self.pop('algorithm', None)
        else:
            self['algorithm'] = name

    #
    #   binary data
    #

    @property
    def data(self) -> Optional[bytes]:
        if self.__data is None:
            text = self.get_str(key='data', default='')
            if len(text) > 0:
                alg = self.algorithm
                if alg == TransportableData.BASE_64:
                    self.__data = base64_decode(string=text)
                elif alg == TransportableData.BASE_58:
                    self.__data = base58_decode(string=text)
                elif alg == TransportableData.HEX:
                    self.__data = hex_decode(string=text)
                else:
                    assert False, 'data algorithm not support: %s' % alg
        return self.__data

    @data.setter
    def data(self, binary: Optional[bytes]):
        if binary is None or len(binary) == 0:
            self.pop('data', None)
        else:
            alg = self.algorithm
            if alg == TransportableData.BASE_64:
                text = base64_encode(data=binary)
            elif alg == TransportableData.BASE_58:
                text = base58_encode(data=binary)
            elif alg == TransportableData.HEX:
                text = hex_encode(data=binary)
            else:
                assert False, 'data algorithm not support: %s' % alg
            self['data'] = text
        self.__data = binary
