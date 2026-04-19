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
from typing import Optional, Dict

from mkm.types import URI
from mkm.format import TransportableData
from mkm.crypto import DecryptKey
from dkd.protocol import Content

from ..format import TransportableFile
from ..format import TransportableFileWrapper
from ..format import PortableNetworkFile

from .types import ContentType
from .base import BaseContent


class FileContent(Content, ABC):
    """
        File Message Content
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0x10),
            "sn"   : 12345,

            "data"     : "...",        // base64_encode(fileContent)
            "filename" : "photo.png",

            "URL"      : "http://...", // download from CDN
            // before fileContent uploaded to a public CDN,
            // it should be encrypted by a symmetric key
            "key"      : {             // symmetric key to decrypt file content
                "algorithm" : "AES",   // "DES", ...
                "data"      : "{BASE64_ENCODE}",
                ...
            }
        }
    """

    @property
    @abstractmethod
    def data(self) -> Optional[TransportableData]:
        # file data (it's too big to set in the dictionary)
        raise NotImplemented

    @data.setter
    @abstractmethod
    def data(self, attachment: Optional[TransportableData]):
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
    #   PNF transforming
    #

    @property
    @abstractmethod
    def transportable_file(self) -> TransportableFile:
        raise NotImplemented

    #
    #  Factories
    #

    @classmethod
    def create(cls, msg_type: str,
               data: Optional[TransportableData] = None, filename: Optional[str] = None,
               url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        if msg_type == ContentType.IMAGE:
            return ImageFileContent(data=data, filename=filename, url=url, password=password)
        elif msg_type == ContentType.AUDIO:
            return AudioFileContent(data=data, filename=filename, url=url, password=password)
        elif msg_type == ContentType.VIDEO:
            return VideoFileContent(data=data, filename=filename, url=url, password=password)
        else:
            return BaseFileContent(msg_type=msg_type, data=data, filename=filename, url=url, password=password)

    @classmethod
    def file(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
             url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        return BaseFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def image(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        return ImageFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def audio(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        return AudioFileContent(data=data, filename=filename, url=url, password=password)

    @classmethod
    def video(cls, data: Optional[TransportableData] = None, filename: Optional[str] = None,
              url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        return VideoFileContent(data=data, filename=filename, url=url, password=password)


class ImageContent(FileContent, ABC):
    """
        Image Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0x12),
            "sn"   : 12345,

            "data"     : "...",        // base64_encode(fileContent)
            "filename" : "photo.png",

            "URL"      : "http://...", // download from CDN
            // before fileContent uploaded to a public CDN,
            // it should be encrypted by a symmetric key
            "key"      : {             // symmetric key to decrypt file content
                "algorithm" : "AES",   // "DES", ...
                "data"      : "{BASE64_ENCODE}",
                ...
            },
            "thumbnail" : "data:image/jpeg;base64,..."
        }
    """

    @property
    @abstractmethod
    def thumbnail(self) -> Optional[TransportableFile]:
        # thumbnail of image
        raise NotImplemented

    @thumbnail.setter
    @abstractmethod
    def thumbnail(self, img: TransportableFile):
        raise NotImplemented


class AudioContent(FileContent, ABC):
    """
        Audio Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0x14),
            "sn"   : 12345,

            "data"     : "...",        // base64_encode(fileContent)
            "filename" : "photo.png",

            "URL"      : "http://...", // download from CDN
            // before fileContent uploaded to a public CDN,
            // it should be encrypted by a symmetric key
            "key"      : {             // symmetric key to decrypt file content
                "algorithm" : "AES",   // "DES", ...
                "data"      : "{BASE64_ENCODE}",
                ...
            },
            "text"     : "..."         // Automatic Speech Recognition
        }
    """

    @property
    @abstractmethod
    def text(self) -> Optional[str]:
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
            "type" : i2s(0x16),
            "sn"   : 12345,

            "data"     : "...",        // base64_encode(fileContent)
            "filename" : "photo.png",

            "URL"      : "http://...", // download from CDN
            // before fileContent uploaded to a public CDN,
            // it should be encrypted by a symmetric key
            "key"      : {             // symmetric key to decrypt file content
                "algorithm" : "AES",   // "DES", ...
                "data"      : "{BASE64_ENCODE}",
                ...
            },
            "snapshot" : "data:image/jpeg;base64,..."
        }
    """

    @property
    @abstractmethod
    def snapshot(self) -> Optional[TransportableFile]:
        # snapshot of video
        raise NotImplemented

    @snapshot.setter
    @abstractmethod
    def snapshot(self, img: TransportableFile):
        raise NotImplemented


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseFileContent(BaseContent, FileContent):
    """ File Message Content """

    def __init__(self, content: Dict = None,
                 msg_type: str = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        if content is None:
            # 1. new content with type, data, filename, url & password
            if msg_type is None:
                msg_type = ContentType.FILE
            super().__init__(None, msg_type)
            content = super().dictionary
        else:
            # 2. content from network
            assert msg_type is None and data is None and filename is None and url is None and password is None, \
                'params error: %s, %s, %s, %s, %s, %s' % (content, msg_type, data, filename, url, password)
            super().__init__(content)
        # access via the wrapper
        wrapper = TransportableFileWrapper.create(content, data=data, filename=filename, url=url, password=password)
        self.__wrapper = wrapper

    @property  # Override
    def dictionary(self) -> Dict:
        """ call wrapper to serialize 'data' & 'key" """
        wrapper = self.__wrapper
        return wrapper.dictionary

    @property  # Override
    def transportable_file(self) -> TransportableFile:
        """ clone without serializations """
        info = super().dictionary
        wrapper = self.__wrapper
        return PortableNetworkFile(dictionary=info, wrapper=wrapper)

    @property  # Override
    def data(self) -> Optional[TransportableData]:
        wrapper = self.__wrapper
        return wrapper.data

    @data.setter  # Override
    def data(self, attachment: TransportableData):
        wrapper = self.__wrapper
        wrapper.data = attachment

    @property  # Override
    def filename(self) -> Optional[str]:
        wrapper = self.__wrapper
        return wrapper.filename

    @filename.setter  # Override
    def filename(self, name: str):
        wrapper = self.__wrapper
        wrapper.filename = name

    @property  # Override
    def url(self) -> Optional[URI]:
        wrapper = self.__wrapper
        return wrapper.url

    @url.setter  # Override
    def url(self, remote: str):
        wrapper = self.__wrapper
        wrapper.url = remote

    @property  # Override
    def password(self) -> Optional[DecryptKey]:
        wrapper = self.__wrapper
        return wrapper.password

    @password.setter  # Override
    def password(self, key: DecryptKey):
        wrapper = self.__wrapper
        wrapper.password = key


class ImageFileContent(BaseFileContent, ImageContent):
    """ Image Message Content """

    def __init__(self, content: Dict = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.IMAGE if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)
        # small image
        self.__thumbnail: Optional[TransportableFile] = None

    @property  # Override
    def dictionary(self) -> Dict:
        # serialize 'thumbnail'
        img = self.__thumbnail
        if img is not None and self.get('thumbnail') is None:
            self['thumbnail'] = img.serialize()
        # OK
        return super().dictionary

    @property  # Override
    def transportable_file(self) -> TransportableFile:
        # serialize 'thumbnail'
        img = self.__thumbnail
        if img is not None and self.get('thumbnail') is None:
            self['thumbnail'] = img.serialize()
        # clone without other serializations
        return super().transportable_file

    @property  # Override
    def thumbnail(self) -> Optional[TransportableFile]:
        img = self.__thumbnail
        if img is None:
            base64 = self.get('thumbnail')
            img = TransportableFile.parse(base64)
            self.__thumbnail = img
        return img

    @thumbnail.setter  # Override
    def thumbnail(self, img: TransportableFile):
        self.pop('thumbnail', None)
        # self['thumbnail'] = None if img is None else img.serialize()
        self.__thumbnail = img


class AudioFileContent(BaseFileContent, AudioContent):
    """ Audio Message Content """

    def __init__(self, content: Dict = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.AUDIO if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)

    @property  # Override
    def text(self) -> Optional[str]:
        return self.get_str(key='text')

    @text.setter  # Override
    def text(self, asr: str):
        self['text'] = asr


class VideoFileContent(BaseFileContent, VideoContent):
    """ Video Message Content """

    def __init__(self, content: Dict = None,
                 data: Optional[TransportableData] = None, filename: Optional[str] = None,
                 url: Optional[URI] = None, password: Optional[DecryptKey] = None):
        msg_type = ContentType.VIDEO if content is None else None
        super().__init__(content, msg_type, data=data, filename=filename, url=url, password=password)
        # small image
        self.__snapshot: Optional[TransportableFile] = None

    @property  # Override
    def dictionary(self) -> Dict:
        # serialize 'snapshot'
        img = self.__snapshot
        if img is not None and self.get('snapshot') is None:
            self['snapshot'] = img.serialize()
        # OK
        return super().dictionary

    @property  # Override
    def transportable_file(self) -> TransportableFile:
        # serialize 'snapshot'
        img = self.__snapshot
        if img is not None and self.get('snapshot') is None:
            self['snapshot'] = img.serialize()
        # clone without other serializations
        return super().transportable_file

    @property  # Override
    def snapshot(self) -> Optional[TransportableFile]:
        img = self.__snapshot
        if img is None:
            base64 = self.get('snapshot')
            img = TransportableFile.parse(base64)
            self.__snapshot = img
        return img

    @snapshot.setter  # Override
    def snapshot(self, img: TransportableFile):
        self.pop('snapshot', None)
        # self['snapshot'] = None if img is None else img.serialize()
        self.__snapshot = img
