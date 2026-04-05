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

from typing import Optional, Any, Dict

from mkm.types import URI, Mapper, Converter
from mkm.crypto import SymmetricKey, DecryptKey
from mkm.format import TransportableData
from mkm.ext import FormatExtensions

from .file_wrapper import TransportableFileWrapper
from .file_wrapper import TransportableFileWrapperFactory


class PortableNetworkFileWrapper(TransportableFileWrapper):

    def __init__(self, dictionary: Dict):
        super().__init__()
        if isinstance(dictionary, Mapper):
            dictionary = dictionary.dictionary
        self.__dictionary = dictionary
        # lazy load
        self.__attachment: Optional[TransportableData] = None
        self.__password: Optional[DecryptKey] = None

    def get_str(self, key: str, default: Optional[str] = None) -> Optional[str]:
        value = self.__dictionary.get(key)
        return Converter.get_str(value=value, default=default)

    def set_map(self, key: str, value: Optional[Mapper]):
        if value is None:
            self.__dictionary.pop(key, None)
        else:
            self.__dictionary[key] = value.dictionary

    # Override
    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """ Return the value for key if key is in the dictionary, else default. """
        return self.__dictionary.get(key, default)

    # Override
    def pop(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        return self.__dictionary.pop(key, default)

    def __contains__(self, o) -> bool:
        """ True if the dictionary has the specified key, else False. """
        return self.__dictionary.__contains__(o)

    def __delitem__(self, v: str):
        """ Delete self[key]. """
        self.__dictionary.__delitem__(v)

    def __getitem__(self, k: str) -> Any:
        """ x.__getitem__(y) <==> x[y] """
        return self.__dictionary.__getitem__(k)

    def __setitem__(self, k: str, v: Optional[Any]):
        """ Set self[key] to value. """
        self.__dictionary.__setitem__(k, v)

    def __sizeof__(self) -> int:
        """ D.__sizeof__() -> size of D in memory, in bytes """
        return self.__dictionary.__sizeof__()

    def __len__(self) -> int:
        """ Return len(self). """
        return self.__dictionary.__len__()

    __hash__ = None

    # Override
    @property
    def dictionary(self) -> Dict:
        info = self.__dictionary
        # serialize 'data'
        ted = self.__attachment
        if ted is not None and info.get('data') is None:
            info['data'] = ted.serialize()
        # serialize 'key'
        pwd = self.__password
        if pwd is not None and info.get('key') is None:
            info['key'] = pwd.dictionary
        # OK
        return info

    #
    #   File data
    #

    # Override
    @property
    def data(self) -> Optional[TransportableData]:
        ted = self.__attachment
        if ted is None:
            base64 = self.__dictionary.get('data')
            ted = TransportableData.parse(base64)
            self.__attachment = ted
        return ted

    # Override
    @data.setter
    def data(self, content: Optional[TransportableData]):
        self.__dictionary.pop('data', None)
        # self.__dictionary['data'] = None if content is None else content.serialize()
        self.__attachment = content

    #
    #   File name
    #

    # Override
    @property
    def filename(self) -> Optional[str]:
        return self.get_str(key='filename')

    # Override
    @filename.setter
    def filename(self, name: Optional[str]):
        if name is None:
            self.__dictionary.pop('filename', None)
        else:
            self.__dictionary['filename'] = name

    #
    #   Download URL
    #

    # Override
    @property
    def url(self) -> Optional[URI]:
        # TODO: convert str to URI?
        return self.get_str(key='URL')

    # Override
    @url.setter
    def url(self, remote: Optional[URI]):
        if remote is None:
            self.__dictionary.pop('URL', None)
        else:
            # TODO: convert URI to str?
            self.__dictionary['URL'] = remote

    #
    #   Decrypt Key
    #

    # Override
    @property
    def password(self) -> Optional[DecryptKey]:
        key = self.__password
        if key is None:
            info = self.__dictionary.get('key')
            key = SymmetricKey.parse(key=info)
            self.__password = key
        return key

    # Override
    @password.setter
    def password(self, key: Optional[DecryptKey]):
        self.__dictionary.pop('key', None)
        # self.__dictionary['key'] = None if key is None else key.dictionary
        # self.set_map(key='key', value=key)
        self.__password = key


# -----------------------------------------------------------------------------
#  Format Extensions
# -----------------------------------------------------------------------------


class _PNFWrapperFactory(TransportableFileWrapperFactory):

    # Override
    def create_transportable_file_wrapper(self, content: Dict,
                                          data: Optional[TransportableData],
                                          filename: Optional[str],
                                          url: Optional[URI],
                                          password: Optional[DecryptKey]) -> TransportableFileWrapper:
        # create wrapper for the content
        wrapper = PortableNetworkFileWrapper(content)
        # file data
        if data is not None:
            wrapper.data = data
        # file name
        if filename is not None:
            wrapper.filename = filename
        # remote URL
        if url is not None:
            wrapper.url = url
        # decrypt key
        if password is not None:
            wrapper.password = password
        # OK
        return wrapper


class _WrapperExt:
    _wrapper_factory: TransportableFileWrapperFactory = _PNFWrapperFactory()

    @property
    def wrapper_factory(self) -> TransportableFileWrapperFactory:
        return _WrapperExt._wrapper_factory

    @wrapper_factory.setter
    def wrapper_factory(self, factory: TransportableFileWrapperFactory):
        _WrapperExt._wrapper_factory = factory


FormatExtensions.pnf_wrapper_factory = _WrapperExt.wrapper_factory
