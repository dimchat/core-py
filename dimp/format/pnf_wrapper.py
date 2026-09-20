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
from typing import Optional

from mkm.types import URI
from mkm.types import StrMap, MutableStrMap

from mkm.crypto import DecryptKey
from mkm.format import TransportableData
from mkm.ext import shared_format_extensions


# -----------------------------------------------------------------------------
#  PNF Wrapper
# -----------------------------------------------------------------------------

class TransportableFileWrapper(ABC):
    """
    A wrapper interface for serializing/deserializing `TransportableFile`
    data to/from a Map.

    The serialized Map follows this structure:

    .. code-block:: json

        {
          "data": "<base64-encoded file content>", // From `TransportableData`
          "filename": "photo.png",                 // Original file name

          "URL": "http://example.com/photo.png",   // Remote CDN URL (alternative to `data`)
          "key": {                                 // Symmetric decryption key (for encrypted CDN content)
            "algorithm": "AES",                    // Encryption algorithm (e.g., "AES", "DES")
            "data": "<base64-encoded key data>"    // Key material (base64 encoded)
          }
        }

    Key notes:
    - `data` and `URL` are mutually exclusive for large files
      (prefer `URL` to reduce payload size)
    - `key` is required only if the CDN-hosted content is encrypted
    """

    @abstractmethod
    def to_map(self) -> MutableStrMap:
        """
        Converts the wrapper's state to a structured Map
        (matches the format defined in this class).

        Core logic:
        - Serializes the `data` property (TransportableData) into the "data"
          field of the Map
        - Subclasses may override this method to implement lazy serialization
          for other properties (e.g., defer encoding large file data until
          this method is called)

        Returns a serialized Map containing the file metadata and
        serialized `data`.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.to_map()'
        )

    #
    #   File data
    #

    @property
    @abstractmethod
    def data(self) -> Optional[TransportableData]:
        """
        Binary file data (encoded as `TransportableData`).

        For large files, use `url` instead to avoid large payloads.
        """
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
        Remote CDN URL to download the file (alternative to `data`
        for large files).
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
    #   Decrypt Key
    #

    @property
    @abstractmethod
    def password(self) -> Optional[DecryptKey]:
        """
        Symmetric decryption key for encrypted file content from `url`.

        Aliased as `password` for legacy compatibility
        (actual value is a `DecryptKey`).
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

    #
    #  Factory method
    #

    @classmethod
    def create(cls, content: StrMap,
               data: Optional[TransportableData] = None,
               filename: Optional[str] = None,
               url: Optional[URI] = None,
               password: Optional[DecryptKey] = None):
        factory = pnf_wrapper_factory()
        return factory.create_transportable_file_wrapper(content,
                                                         data=data, filename=filename,
                                                         url=url, password=password)


class TransportableFileWrapperFactory(ABC):
    """
    Factory interface for creating `TransportableFileWrapper` instances.

    Implement this interface to provide custom wrapper implementations
    (e.g., for different serialization formats).
    """

    @abstractmethod
    def create_transportable_file_wrapper(self, content: StrMap,
                                          data: Optional[TransportableData],
                                          filename: Optional[str],
                                          url: Optional[URI],
                                          password: Optional[DecryptKey]) -> TransportableFileWrapper:
        """
        Creates a `TransportableFileWrapper` instance with the given parameters.

        `content` is the base Map to initialize the wrapper
        (may contain partial metadata).
        `data` is the binary file data (overrides ``content["data"]`` if provided).
        `filename` is the original file name (overrides ``content["filename"]`` if provided).
        `url` is the remote CDN URL (overrides ``content["URL"]`` if provided).
        `password` is the decryption key (overrides ``content["key"]`` if provided).

        Returns a custom `TransportableFileWrapper` implementation.
        """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.create_transportable_file_wrapper()'
        )


# -----------------------------------------------------------------------------
#  Format Extensions
# -----------------------------------------------------------------------------


class TransportableFileWrapperExtension:

    @property
    def pnf_wrapper_factory(self) -> Optional[TransportableFileWrapperFactory]:
        """ Get PNF wrapper factory """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.pnf_wrapper_factory getter'
        )

    @pnf_wrapper_factory.setter
    def pnf_wrapper_factory(self, factory: TransportableFileWrapperFactory):
        """ Set PNF wrapper factory """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.pnf_wrapper_factory setter'
        )


shared_format_extensions.pnf_wrapper_factory: Optional[TransportableFileWrapperFactory] = None


def _pnf_wrapper_extension() -> TransportableFileWrapperExtension:
    return shared_format_extensions


def pnf_wrapper_factory() -> TransportableFileWrapperFactory:
    ext = _pnf_wrapper_extension()
    return ext.pnf_wrapper_factory
