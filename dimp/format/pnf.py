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
from typing import Optional, Union, Any

from mkm.types import StrMap, MutableStrMap
from mkm.types import Mapper
from mkm.types import URI

from mkm.crypto import DecryptKey
from mkm.format import TransportableResource
from mkm.format import TransportableData
from mkm.ext import shared_format_extensions


class TransportableFile(Mapper, TransportableResource, ABC):
    """
        Portable Network File (PNF) - transportable file with metadata
        and encryption support.

        Extends `TransportableResource` to represent files with additional
        metadata (filename, URL, encryption key) for network transmission.

        Supported formats (extends `TransportableResource`):
         2. Data URI format: ``"data:image/png;base64,{BASE64_ENCODE}"``
         3. Structured JSON object (with metadata and encryption):

        .. code-block:: json

            {
              "data"     : "...",         // Base64-encoded file content
              "filename" : "avatar.png",
              "URL"      : "http://...",  // CDN download URL (alternative to inline data)
              "key"      : {              // Symmetric encryption key (for encrypted content)
                "algorithm" : "AES",      // Encryption algorithm (e.g., "AES", "DES")
                "data"      : "{BASE64_ENCODE}"
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
        """
        Binary file data (encoded as `TransportableData`).

        For large files, it's recommended to use `url` instead of inline `data`
        to reduce payload size (upload to CDN first, then reference via URL).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.data getter'
        )

    @data.setter
    @abstractmethod
    def data(self, content: Optional[TransportableData]):
        """ Set file data """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.data setter'
        )

    @property
    @abstractmethod
    def filename(self) -> Optional[str]:
        """ Original filename of the file (e.g., "avatar.png"). """
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
        """
        Remote URL to download the file (typically from CDN).

        Alternative to inline `data` for large files.
        """
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
    #   Password for decrypting the downloaded data from CDN,
    #   default is a plain key, which just return the same data when decrypting.
    #
    @property
    @abstractmethod
    def password(self) -> Optional[DecryptKey]:
        """
        Decryption key for encrypted file content from CDN.

        Defaults to a plain key (returns original data when decrypted)
        if not specified.
        """
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

    # Override
    @abstractmethod
    def __str__(self) -> str:
        """
        Returns string representation of the PNF.

        Returns the URL string (if only `url` and `filename` are present),
        or the JSON string of the structured object (for full metadata).

        :return: 'URL', or JSON string: '{...}'
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.__str__()'
        )

    # Override
    @abstractmethod
    def to_map(self) -> MutableStrMap:
        """
        Converts the PNF to a structured Map (format 3).

        Core logic:
        - Serializes the `data` property (TransportableData) into the "data"
          field of the Map
        - Subclasses may override this method to implement lazy serialization
          for other properties (e.g., defer encoding large file data until
          this method is called)
        - Updates internal state with the serialized `data` before returning
          the Map

        Returns a Map representation of the PNF (matches JSON structure).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_map()'
        )

    # Override
    @abstractmethod
    def serialize(self) -> Union[str, StrMap]:
        """
        Serializes the PNF to a transportable format.

        Serialization logic:
        - If only `url` and `filename` exist: returns URL string (str())
        - Otherwise: returns structured Map (to_map())

        :return: str or dict
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.serialize()'
        )

    #
    #  Factory methods
    #

    @classmethod
    def create_from_url(cls, url: URI, password: Optional[DecryptKey]):
        """ Create from remote URL """
        return cls.create(url=url, password=password)

    @classmethod
    def create_from_data(cls, data: TransportableData, filename: Optional[str]):
        """ Create from file data """
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


class TransportableFileFactory(ABC):
    """
    Factory interface for creating `TransportableFile` (PNF) instances.
    """

    @abstractmethod
    def parse_transportable_file(self, pnf: StrMap) -> Optional[TransportableFile]:
        """
        Parses a structured Map into a `TransportableFile` instance.

        `pnf` is the Map representation of PNF (matches format 3 JSON structure).

        Returns a `TransportableFile` instance, or None if parsing fails.

        :param pnf: PNF info
        :return: PNF object
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_transportable_file()'
        )

    @abstractmethod
    def create_transportable_file(self, data: Optional[TransportableData], filename: Optional[str],
                                  url: Optional[URI], password: Optional[DecryptKey]) -> TransportableFile:
        """
        Creates a `TransportableFile` instance with the given parameters.

        `data` is the encoded file content (null if using `url` instead).
        `filename` is the original filename of the file.
        `url` is the CDN download URL (alternative to `data`).
        `password` is the decryption key for encrypted content.

        Returns a new `TransportableFile` instance.

        :param data:     file data (not encrypted)
        :param filename: file name
        :param url:      download URL
        :param password: decrypt key for downloaded data
        :return: PNF object
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_transportable_file()'
        )


# -----------------------------------------------------------------------------
#  Format Extensions
# -----------------------------------------------------------------------------


class TransportableFileHelper(ABC):
    """
    Helper interface for creating/parsing `TransportableFile` instances.

    Provides factory methods to abstract the creation logic of
    `TransportableFile` implementations.
    """

    @abstractmethod
    def set_transportable_file_factory(self, factory: TransportableFileFactory):
        """ Set transportable file factory """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.set_transportable_file_factory()'
        )

    @abstractmethod
    def get_transportable_file_factory(self) -> Optional[TransportableFileFactory]:
        """ Get transportable file factory """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.get_transportable_file_factory()'
        )

    @abstractmethod
    def create_transportable_file(self, data: Optional[TransportableData], filename: Optional[str],
                                  url: Optional[URI], password: Optional[DecryptKey]) -> TransportableFile:
        """
        Creates a `TransportableFile` instance with the given metadata.

        `data` is the binary file data (encoded as `TransportableData`).
        `filename` is the original file name (e.g., "document.pdf").
        `url` is the remote CDN URL (alternative to `data` for large files).
        `password` is the decryption key for encrypted CDN content.

        Returns an initialized `TransportableFile` instance.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_transportable_file()'
        )

    @abstractmethod
    def parse_transportable_file(self, pnf: Any) -> Optional[TransportableFile]:
        """
        Parses a raw object into a `TransportableFile` instance.

        Converts arbitrary raw data (e.g., string, map) into a standardized
        TransportableFile object.

        `pnf` is the raw data object to parse.

        Returns a parsed `TransportableFile` instance (null if parsing fails).
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.parse_transportable_file()'
        )


class TransportableFileExtension:

    @property
    def pnf_helper(self) -> Optional[TransportableFileHelper]:
        """ Get PNF helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.pnf_helper getter'
        )

    @pnf_helper.setter
    def pnf_helper(self, helper: TransportableFileHelper):
        """ Set PNF helper """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.pnf_helper setter'
        )


shared_format_extensions.pnf_helper: Optional[TransportableFileHelper] = None


def format_extensions() -> TransportableFileExtension:
    return shared_format_extensions


def pnf_helper() -> TransportableFileHelper:
    ext = format_extensions()
    return ext.pnf_helper
