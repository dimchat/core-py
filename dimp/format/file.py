# -*- coding: utf-8 -*-
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

from abc import ABC, abstractmethod
from typing import Optional, Union, Any, Dict

from mkm.types import Mapper
from mkm.types import URI
from mkm.crypto import DecryptKey
from mkm.format import TransportableResource
from mkm.format import TransportableData
from mkm.ext import FormatExtensions, shared_format_extensions


class TransportableFile(Mapper, TransportableResource, ABC):
    """
        Transportable File
        ~~~~~~~~~~~~~~~~~~
        PNF - Portable Network File

            2. "https://..."
            3. {
                data     : "...",        // base64_encode(fileContent)
                filename : "avatar.png",

                URL      : "http://...", // download from CDN
                // before fileContent uploaded to a public CDN,
                // it can be encrypted by a symmetric key
                key      : {             // symmetric key to decrypt file content
                    algorithm : "AES",   // "DES", ...
                    data      : "{BASE64_ENCODE}",
                    ...
                }
            }
    """

    #
    #   When file data is too big, don't set it in this dictionary,
    #   but upload it to a CDN and set the download URL instead.
    #
    @property
    @abstractmethod
    def data(self) -> Optional[TransportableData]:
        raise NotImplemented

    @data.setter
    @abstractmethod
    def data(self, content: Optional[TransportableData]):
        raise NotImplemented

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
    #   Password for decrypting the downloaded data from CDN,
    #   default is a plain key, which just return the same data when decrypting.
    #
    @property
    @abstractmethod
    def password(self) -> Optional[DecryptKey]:
        raise NotImplemented

    @password.setter
    @abstractmethod
    def password(self, key: Optional[DecryptKey]):
        raise NotImplemented

    # Override
    @abstractmethod
    def __str__(self) -> str:
        """
        Get encoded string

        :return: 'URL', or JSON string: '{...}'
        """
        raise NotImplemented

    # Override
    @property
    @abstractmethod
    def dictionary(self) -> Dict:
        """ serialize to map """
        raise NotImplemented

    # Override
    @abstractmethod
    def serialize(self) -> Union[str, dict]:
        """
        Serializes this PNF to a URL string or a map.

        :return: str or dict
        """
        return NotImplemented

    #
    #  Factory methods
    #

    @classmethod
    def create_from_url(cls, url: URI, password: Optional[DecryptKey]):
        return cls.create(url=url, password=password)

    @classmethod
    def create_from_data(cls, data: TransportableData, filename: Optional[str]):
        return cls.create(data=data, filename=filename)

    @classmethod
    def create(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
               url: Optional[URI] = None, password: Optional[DecryptKey] = None):  # -> TransportableFile:
        helper = pnf_helper()
        return helper.create_transportable_file(data=data, filename=filename, url=url, password=password)

    @classmethod
    def parse(cls, pnf: Any):  # -> Optional[TransportableFile]:
        helper = pnf_helper()
        return helper.parse_transportable_file(pnf)

    @classmethod
    def get_factory(cls):  # -> Optional[TransportableFileFactory]:
        helper = pnf_helper()
        return helper.get_transportable_file_factory()

    @classmethod
    def set_factory(cls, factory):
        helper = pnf_helper()
        helper.set_transportable_file_factory(factory=factory)


def pnf_helper():
    helper = shared_format_extensions.pnf_helper
    assert isinstance(helper, TransportableFileHelper), 'PNF helper error: %s' % helper
    return helper


class TransportableFileFactory(ABC):
    """ PNF factory """

    @abstractmethod
    def create_transportable_file(self, data: Optional[TransportableData], filename: Optional[str],
                                  url: Optional[URI], password: Optional[DecryptKey]) -> TransportableFile:
        """
        Create PNF

        :param data:     file data (not encrypted)
        :param filename: file name
        :param url:      download URL
        :param password: decrypt key for downloaded data
        :return: PNF object
        """
        raise NotImplemented

    @abstractmethod
    def parse_transportable_file(self, pnf: Dict) -> Optional[TransportableFile]:
        """
        Parse map object to PNF

        :param pnf: PNF info
        :return: PNF object
        """
        raise NotImplemented


# -----------------------------------------------------------------------------
#  Format Extensions
# -----------------------------------------------------------------------------


class TransportableFileHelper(ABC):
    """ General Helper """

    @abstractmethod
    def set_transportable_file_factory(self, factory: TransportableFileFactory):
        raise NotImplemented

    @abstractmethod
    def get_transportable_file_factory(self) -> Optional[TransportableFileFactory]:
        raise NotImplemented

    @abstractmethod
    def create_transportable_file(self, data: Optional[TransportableData], filename: Optional[str],
                                  url: Optional[URI], password: Optional[DecryptKey]) -> TransportableFile:
        raise NotImplemented

    @abstractmethod
    def parse_transportable_file(self, pnf: Any) -> Optional[TransportableFile]:
        raise NotImplemented


class _PnfExt:
    _pnf_helper: Optional[TransportableFileHelper] = None

    @property
    def pnf_helper(self) -> Optional[TransportableFileHelper]:
        return _PnfExt._pnf_helper

    @pnf_helper.setter
    def pnf_helper(self, helper: TransportableFileHelper):
        _PnfExt._pnf_helper = helper


FormatExtensions.pnf_helper = _PnfExt.pnf_helper
