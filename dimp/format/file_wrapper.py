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

    @abstractmethod
    def to_dict(self) -> Dict:
        """ Serialize to map """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_dict()'
        )

    #
    #   File data
    #

    @property
    @abstractmethod
    def data(self) -> Optional[TransportableData]:
        """ Get binary file content """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.data getter'
        )

    @data.setter
    @abstractmethod
    def data(self, content: Optional[TransportableData]):
        """ Set binary file content """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.data setter'
        )

    #
    #   File name
    #

    @property
    @abstractmethod
    def filename(self) -> Optional[str]:
        """ Get filename """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.filename getter'
        )

    @filename.setter
    @abstractmethod
    def filename(self, string: Optional[str]):
        """ Set filename """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.filename setter'
        )

    #
    #   Download URL
    #

    @property
    @abstractmethod
    def url(self) -> Optional[URI]:
        """ Get download URL from CDN """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.url getter'
        )

    @url.setter
    @abstractmethod
    def url(self, string: Optional[URI]):
        """ Set URL """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.url setter'
        )

    #
    #   Decrypt Key
    #

    @property
    @abstractmethod
    def password(self) -> Optional[DecryptKey]:
        """ Get password """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.password getter'
        )

    @password.setter
    @abstractmethod
    def password(self, key: Optional[DecryptKey]):
        """ Set password """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.password setter'
        )

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


class TransportableFileWrapperFactory(ABC):
    """ Wrapper factory """

    @abstractmethod
    def create_transportable_file_wrapper(self, content: Dict,
                                          data: Optional[TransportableData],
                                          filename: Optional[str],
                                          url: Optional[URI],
                                          password: Optional[DecryptKey]) -> TransportableFileWrapper:
        """ Create PNF wrapper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_transportable_file_wrapper()'
        )


# -----------------------------------------------------------------------------
#  Format Extensions
# -----------------------------------------------------------------------------


class TransportableFileWrapperExtension:

    @property
    def pnf_wrapper_factory(self) -> Optional[TransportableFileWrapperFactory]:
        """ Get factory for PNF wrapper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.pnf_wrapper_factory getter'
        )

    @pnf_wrapper_factory.setter
    def pnf_wrapper_factory(self, factory: TransportableFileWrapperFactory):
        """ Set factory for PNF wrapper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.pnf_wrapper_factory setter'
        )


shared_format_extensions.pnf_wrapper_factory: Optional[TransportableFileWrapperFactory] = None


def format_extensions() -> TransportableFileWrapperExtension:
    return shared_format_extensions


def wrapper_factory() -> TransportableFileWrapperFactory:
    ext = format_extensions()
    return ext.pnf_wrapper_factory
    # return shared_format_extensions.pnf_wrapper_factory


def set_wrapper_factory(factory: TransportableFileWrapperFactory):
    ext = format_extensions()
    ext.pnf_wrapper_factory = factory
    # shared_format_extensions.pnf_wrapper_factory = factory
