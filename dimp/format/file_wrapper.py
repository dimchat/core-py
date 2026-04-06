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
from typing import Optional, Dict

from mkm.types import URI
from mkm.crypto import DecryptKey
from mkm.format import TransportableData
from mkm.ext import shared_format_extensions


class TransportableFileWrapper(ABC):

    @property
    @abstractmethod
    def dictionary(self) -> Dict:
        """ serialize to map """
        raise NotImplemented

    #
    #   File data
    #

    @property
    @abstractmethod
    def data(self) -> Optional[TransportableData]:
        """ binary file content """
        raise NotImplemented

    @data.setter
    @abstractmethod
    def data(self, content: Optional[TransportableData]):
        raise NotImplemented

    #
    #   File name
    #

    @property
    @abstractmethod
    def filename(self) -> Optional[str]:
        raise NotImplemented

    @filename.setter
    @abstractmethod
    def filename(self, string: Optional[str]):
        raise NotImplemented

    #
    #   Download URL
    #

    @property
    @abstractmethod
    def url(self) -> Optional[URI]:
        # download URL from CDN
        raise NotImplemented

    @url.setter
    @abstractmethod
    def url(self, string: Optional[URI]):
        raise NotImplemented

    #
    #   Decrypt Key
    #

    @property
    @abstractmethod
    def password(self) -> Optional[DecryptKey]:
        raise NotImplemented

    @password.setter
    @abstractmethod
    def password(self, key: Optional[DecryptKey]):
        raise NotImplemented

    #
    #  Factory method
    #

    @classmethod
    def create(cls, content: Dict,
               data: Optional[TransportableData] = None, filename: Optional[str] = None,
               url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        factory = wrapper_factory()
        return factory.create_transportable_file_wrapper(content,
                                                         data=data, filename=filename,
                                                         url=url, password=password)


def wrapper_factory():
    factory = shared_format_extensions.pnf_wrapper_factory
    assert isinstance(factory, TransportableFileWrapperFactory), 'PNF wrapper factory error: %s' % factory
    return factory


class TransportableFileWrapperFactory(ABC):
    """ Wrapper factory """

    @abstractmethod
    def create_transportable_file_wrapper(self, content: Dict,
                                          data: Optional[TransportableData],
                                          filename: Optional[str],
                                          url: Optional[URI],
                                          password: Optional[DecryptKey]) -> TransportableFileWrapper:
        raise NotImplemented
