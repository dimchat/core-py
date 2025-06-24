# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
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
from mkm.format import TransportableData
from mkm.format import PortableNetworkFile
from mkm.crypto import DecryptKey
from dkd import Content

from .types import ContentType


class FileContent(Content, ABC):
    """
        File Message Content
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x10),
            sn   : 123,

            data     : "...",        // base64_encode(fileContent)
            filename : "photo.png",

            URL      : "http://...", // download from CDN
            // before fileContent uploaded to a public CDN,
            // it should be encrypted by a symmetric key
            key      : {             // symmetric key to decrypt file content
                algorithm : "AES",   // "DES", ...
                data      : "{BASE64_ENCODE}",
                ...
            }
        }
    """

    @property
    @abstractmethod
    def data(self) -> Optional[bytes]:
        # file data (it's too big to set in the dictionary)
        raise NotImplemented

    @data.setter
    @abstractmethod
    def data(self, attachment: Optional[bytes]):
        raise NotImplemented

    @property
    @abstractmethod
    def filename(self) -> Optional[str]:
        raise NotImplemented

    @filename.setter
    @abstractmethod
    def filename(self, name: str):
        raise NotImplemented

    @property
    @abstractmethod
    def url(self) -> Optional[URI]:
        raise NotImplemented

    @url.setter
    @abstractmethod
    def url(self, remote: URI):
        raise NotImplemented

    @property
    @abstractmethod
    def password(self) -> Optional[DecryptKey]:
        """ symmetric key to decrypt the encrypted data from URL """
        raise NotImplemented

    @password.setter
    @abstractmethod
    def password(self, key: DecryptKey):
        raise NotImplemented

    #
    #  Factories
    #

    @classmethod
    def create(cls, msg_type: str,
               data: Optional[TransportableData] = None, filename: Optional[str] = None,
               url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        if msg_type == ContentType.IMAGE:
            from ..dkd import ImageFileContent
            return ImageFileContent(data=data, filename=filename, url=url, password=password)
        elif msg_type == ContentType.AUDIO:
            from ..dkd import AudioFileContent
            return AudioFileContent(data=data, filename=filename, url=url, password=password)
        elif msg_type == ContentType.VIDEO:
            from ..dkd import VideoFileContent
            return VideoFileContent(data=data, filename=filename, url=url, password=password)
        else:
            from ..dkd import BaseFileContent
            return BaseFileContent(msg_type=msg_type, data=data, filename=filename, url=url, password=password)

    @classmethod
    def file(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
             url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        from ..dkd import BaseFileContent
        return BaseFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def image(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        from ..dkd import ImageFileContent
        return ImageFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def audio(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        from ..dkd import AudioFileContent
        return AudioFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def video(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        from ..dkd import VideoFileContent
        return VideoFileContent(data=data, filename=filename, url=url, password=password)


class ImageContent(FileContent, ABC):
    """
        Image Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x12),
            sn   : 123,

            data     : "...",        // base64_encode(fileContent)
            filename : "photo.png",

            URL      : "http://...", // download from CDN
            // before fileContent uploaded to a public CDN,
            // it should be encrypted by a symmetric key
            key      : {             // symmetric key to decrypt file content
                algorithm : "AES",   // "DES", ...
                data      : "{BASE64_ENCODE}",
                ...
            },
            thumbnail : "data:image/jpeg;base64,..."
        }
    """

    @property
    @abstractmethod
    def thumbnail(self) -> Optional[PortableNetworkFile]:
        # thumbnail of image
        raise NotImplemented

    @thumbnail.setter
    @abstractmethod
    def thumbnail(self, img: PortableNetworkFile):
        raise NotImplemented


class AudioContent(FileContent, ABC):
    """
        Audio Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x14),
            sn   : 123,

            data     : "...",        // base64_encode(fileContent)
            filename : "photo.png",

            URL      : "http://...", // download from CDN
            // before fileContent uploaded to a public CDN,
            // it should be encrypted by a symmetric key
            key      : {             // symmetric key to decrypt file content
                algorithm : "AES",   // "DES", ...
                data      : "{BASE64_ENCODE}",
                ...
            },
            text     : "..."         // Automatic Speech Recognition
        }
    """

    @property
    @abstractmethod
    def text(self) -> Optional[bytes]:
        # Automatic Speech Recognition
        raise NotImplemented

    @text.setter
    @abstractmethod
    def text(self, asr: str):
        raise NotImplemented


class VideoContent(FileContent, ABC):
    """
        Video Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x16),
            sn   : 123,

            data     : "...",        // base64_encode(fileContent)
            filename : "photo.png",

            URL      : "http://...", // download from CDN
            // before fileContent uploaded to a public CDN,
            // it should be encrypted by a symmetric key
            key      : {             // symmetric key to decrypt file content
                algorithm : "AES",   // "DES", ...
                data      : "{BASE64_ENCODE}",
                ...
            },
            snapshot : "data:image/jpeg;base64,..."
        }
    """

    @property
    @abstractmethod
    def snapshot(self) -> Optional[PortableNetworkFile]:
        # snapshot of video
        raise NotImplemented

    @snapshot.setter
    @abstractmethod
    def snapshot(self, img: PortableNetworkFile):
        raise NotImplemented
