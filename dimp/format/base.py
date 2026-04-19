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

from abc import ABC, abstractmethod
from typing import Optional

from mkm.types import Stringer
from mkm.format import TransportableData


class EncodeAlgorithms:
    """ Algorithms for Encoding Data """

    DEFAULT = 'base64'

    BASE_64 = 'base64'
    BASE_58 = 'base58'
    HEX = 'hex'


class BaseString(Stringer):

    def __init__(self, string: Optional[str]):
        super().__init__()
        # protected
        self._string = string  # encoded string

    @property  # protected
    def inner_string(self) -> Optional[str]:
        return self._string

    # Override
    def to_str(self) -> str:
        s = self._string
        return '' if s is None else s

    # Override
    def __hash__(self) -> int:
        """ Return hash(self). """
        s = self.to_str()
        return s.__hash__()

    # Override
    def __len__(self) -> int:
        """ Return len(self). """
        s = self.to_str()
        return s.__len__()

    # Override
    def __eq__(self, x: str) -> bool:
        """ Return self==value. """
        if isinstance(x, Stringer):
            if self is x:
                # same object
                return True
            x = x.to_str()
        # check inner string
        s = self.to_str()
        return s.__eq__(x)

    # Override
    def __ne__(self, x: str) -> bool:
        """ Return self!=value. """
        if isinstance(x, Stringer):
            if self is x:
                # same object
                return False
            x = x.to_str()
        # check inner string
        s = self.to_str()
        return s.__ne__(x)

    # Override
    def __str__(self) -> str:
        """ Return str(self). """
        return self.to_str()

    # Override
    def __repr__(self) -> str:
        """ Return repr(self). """
        clazz = self.__class__.__name__
        return '<%s>%s</%s>' % (clazz, self.to_str(), clazz)


class BaseData(BaseString, TransportableData, ABC):

    def __init__(self, string: Optional[str], binary: Optional[bytes]):
        super().__init__(string=string)
        # protected
        self._binary = binary  # decoded bytes

    @property  # protected
    def inner_binary(self) -> Optional[bytes]:
        return self._binary

    # Override
    @abstractmethod
    def to_str(self) -> str:
        raise NotImplemented

    @property
    def is_empty(self) -> bool:
        binary = self.inner_binary
        if binary is not None and len(binary) > 0:
            return False
        string = self.inner_string
        return string is None or len(string) == 0

    # Override
    def serialize(self) -> str:
        return self.to_str()

    # Override
    def __len__(self) -> int:
        """ Return len(self). """
        return len(self.to_bytes())

    # Override
    def __hash__(self) -> int:
        """ Return hash(self). """
        return hash(self.to_str())

    # Override
    def __eq__(self, x: str) -> bool:
        """ Return self==value. """
        if self is x:
            # same object
            return True
        elif isinstance(x, BaseData):
            # compare as base data
            return _data_equals(this=self, that=x)
        elif isinstance(x, TransportableData):
            # compare as ted
            return _ted_equals(this=self, that=x)
        elif isinstance(x, Stringer):
            # compare with inner string
            return self.to_str() == x.to_str()
        # check inner string
        return self.to_str() == x

    # Override
    def __ne__(self, x: str) -> bool:
        """ Return self!=value. """
        if self is x:
            # same object
            return False
        elif isinstance(x, BaseData):
            # compare as base data
            return not _data_equals(this=self, that=x)
        elif isinstance(x, TransportableData):
            # compare as ted
            return not _ted_equals(this=self, that=x)
        elif isinstance(x, Stringer):
            # compare with inner string
            return self.to_str() != x.to_str()
        # check inner string
        return self.to_str() != x


def _data_equals(this: BaseData, that: BaseData) -> bool:
    if that is None or that.is_empty:
        return this.is_empty
    # compare with inner string
    this_string = this.inner_string
    that_string = that.inner_string
    if this_string is not None and that_string is not None:
        if len(this_string) > 0 and len(that_string) > 0:
            return this_string == that_string
    # compare with inner bytes
    this_bytes = this.inner_binary
    that_bytes = that.inner_binary
    if this_bytes is not None and that_bytes is not None:
        return this_bytes == that_bytes
    # compare with decoded bytes
    return this.to_bytes() == that.to_bytes()


def _ted_equals(this: BaseData, that: TransportableData) -> bool:
    if that is None or that.is_empty:
        return this.is_empty
    # compare with encoded string
    this_string = this.inner_string
    if this_string is not None and len(this_string) > 0:
        return this_string == that.to_str()
    # compare with encoded bytes
    return this.inner_binary == that.to_str()
