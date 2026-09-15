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


class BaseString(Stringer):
    """
        Base String
        ~~~~~~~~~~~
    """

    def __init__(self, string: Optional[str]):
        super().__init__()
        # encoded string
        self._string = string

    @property  # protected
    def inner_string(self) -> Optional[str]:
        return self._string

    # Override
    def to_str(self) -> str:
        s = self._string
        return '' if s is None else s

    @property  # Override
    def is_empty(self) -> bool:
        text = self.to_str()
        return len(text) == 0

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
    def __eq__(self, other) -> bool:
        """ Return self==value. """
        if other is None:
            return False
        elif self is other:
            # same object
            return True
        # compare as string
        text = self.to_str()
        if isinstance(other, Stringer):
            return text == other.to_str()
        elif isinstance(other, str):
            return text == other
        else:
            return False

    # Override
    def __ne__(self, other) -> bool:
        """ Return self!=value. """
        if other is None:
            return True
        elif self is other:
            return False
        # compare as string
        text = self.to_str()
        if isinstance(other, Stringer):
            return text != other.to_str()
        elif isinstance(other, str):
            return text != other
        else:
            return True

    # Override
    def __str__(self) -> str:
        """ Return str(self). """
        return self.to_str()

    # Override
    def __repr__(self) -> str:
        """ Return repr(self). """
        clazz = self.__class__.__name__
        text = self.to_str()
        return f'<{clazz}>{text}</{clazz}>'


class BaseData(BaseString, TransportableData, ABC):
    """
        Base Data
        ~~~~~~~~~
    """

    def __init__(self, string: Optional[str], binary: Optional[bytes]):
        super().__init__(string=string)
        # decoded bytes
        self._binary = binary

    @property  # protected
    def inner_binary(self) -> Optional[bytes]:
        return self._binary

    # Override
    @abstractmethod
    def to_str(self) -> str:
        """ Convert to string """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_str()'
        )

    @property  # Override
    def is_empty(self) -> bool:
        # 1. check inner bytes
        binary = self.inner_binary
        if binary is not None and len(binary) > 0:
            return False
        # 2. check inner string
        string = self.inner_string
        return string is None or len(string) == 0

    @property
    def length_in_bytes(self) -> int:
        data = self.to_bytes()
        if data is None:
            # assert False, 'transportable data error'
            return 0
        # assert len(data) > 0, 'transportable data empty'
        return len(data)

    # Override
    def __len__(self) -> int:
        """ Return len(self). """
        # s = self.to_str()
        # return s.__len__()
        data = self.to_bytes()
        if data is None:
            # assert False, 'transportable data error'
            return 0
        # assert len(data) > 0, 'transportable data empty'
        return data.__len__()

    @abstractmethod
    def to_bytes(self) -> Optional[bytes]:
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_bytes()'
        )

    def serialize(self) -> str:
        """ Encode to bytes """
        return self.to_str()

    # Override
    def __hash__(self) -> int:
        data = self.to_bytes()
        return 0 if data is None else hash(data)

    # Override
    def __eq__(self, x: str) -> bool:
        """ Return self==value. """
        if self is x:
            # same object
            return True
        elif isinstance(x, BaseData):
            if x.is_empty:
                return self.is_empty
            # compare as base data
            return _data_equals(this=self, that=x)
        elif isinstance(x, TransportableData):
            if x.is_empty:
                return self.is_empty
            # compare as ted
            return _ted_equals(this=self, that=x)
        elif isinstance(x, Stringer):
            if x.is_empty:
                return self.is_empty
            # compare with inner string
            return self.to_str() == x.to_str()
        elif isinstance(x, str):
            if x == '':
                return self.is_empty
        # compare with encoded string
        return self.to_str() == x

    # Override
    def __ne__(self, x: str) -> bool:
        """ Return self!=value. """
        if self is x:
            # same object
            return False
        elif isinstance(x, BaseData):
            if x.is_empty:
                return not self.is_empty
            # compare as base data
            return not _data_equals(this=self, that=x)
        elif isinstance(x, TransportableData):
            if x.is_empty:
                return not self.is_empty
            # compare as ted
            return not _ted_equals(this=self, that=x)
        elif isinstance(x, Stringer):
            if x.is_empty:
                return not self.is_empty
            # compare with inner string
            return self.to_str() != x.to_str()
        elif isinstance(x, str):
            if x == '':
                return not self.is_empty
        # compare with encoded string
        return self.to_str() != x


def _data_equals(this: BaseData, that: BaseData) -> bool:
    assert not (that is None or that.is_empty), f'base data error {that}'
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
    assert not (that is None or that.is_empty), f'base data error {that}'
    # compare with encoded string
    this_string = this.inner_string
    if this_string is not None and len(this_string) > 0:
        return this_string == that.to_str()
    # compare with encoded bytes
    return this.inner_binary == that.to_bytes()
