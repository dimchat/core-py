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
from mkm.protocol import ID
from dkd.protocol import Content

from ..format import TransportableFile

from .types import ContentType
from .base import BaseContent


class TextContent(Content, ABC):
    """
        Text Message Content
        ~~~~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0x01),
            "sn"   : 12345,

            "text" : "..."
        }
    """

    #
    #   text
    #
    @property
    @abstractmethod
    def text(self) -> str:
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, text: str):
        return BaseTextContent(text=text)


class PageContent(Content, ABC):
    """
        Web Page message
        ~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0x20),
            "sn"   : 12345,

            "title" : "...",                // Web title
            "desc"  : "...",
            "icon"  : "data:image/x-icon;base64,...",

            "URL"   : "https://github.com/moky/dimp",

            "HTML"      : "...",            // Web content
            "mime_type" : "text/html",      // Content-Type
            "encoding"  : "utf8",
            "base"      : "about:blank"     // Base URL
        }
    """

    #
    #   Web Title
    #

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplemented

    @title.setter
    @abstractmethod
    def title(self, string: str):
        raise NotImplemented

    #
    #   Fav Icon
    #

    @property
    @abstractmethod
    def icon(self) -> Optional[TransportableFile]:
        raise NotImplemented

    @icon.setter
    @abstractmethod
    def icon(self, img: TransportableFile):
        raise NotImplemented

    #
    #   Description
    #

    @property
    @abstractmethod
    def desc(self) -> Optional[str]:
        raise NotImplemented

    @desc.setter
    @abstractmethod
    def desc(self, text: str):
        raise NotImplemented

    #
    #   Page URL
    #

    @property
    @abstractmethod
    def url(self) -> Optional[URI]:
        raise NotImplemented

    @url.setter
    @abstractmethod
    def url(self, locator: URI):
        raise NotImplemented

    #
    #   Page content
    #

    @property
    @abstractmethod
    def html(self) -> Optional[str]:
        raise NotImplemented

    @html.setter
    @abstractmethod
    def html(self, content: str):
        raise NotImplemented

    #
    #   Factory methods
    #
    @classmethod
    def create(cls, url: Optional[URI], html: Optional[str], title: str,
               desc: Optional[str], icon: Optional[TransportableFile]):
        return WebPageContent(url=url, html=html, title=title, desc=desc, icon=icon)

    @classmethod
    def create_with_url(cls, url: URI, title: str, desc: Optional[str], icon: Optional[TransportableFile]):
        return cls.create(url=url, html=None, title=title, desc=desc, icon=icon)

    @classmethod
    def create_with_html(cls, html: str, title: str, desc: Optional[str], icon: Optional[TransportableFile]):
        return cls.create(url=None, html=html, title=title, desc=desc, icon=icon)


class NameCard(Content, ABC):
    """
        Name Card Content
        ~~~~~~~~~~~~~~~~~

        data format: {
            "type" : i2s(0x33),
            "sn"   : 12345,

            "did"    : "{ID}",        // contact's ID
            "name"   : "{nickname}}", // contact's name
            "avatar" : "{URL}"        // avatar - PNF(URL)
        }
    """

    @property
    @abstractmethod
    def identifier(self) -> ID:
        raise NotImplemented

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def avatar(self) -> Optional[TransportableFile]:
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, identifier: ID, name: str, avatar: Optional[TransportableFile]):
        return NameCardContent(identifier=identifier, name=name, avatar=avatar)


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class BaseTextContent(BaseContent, TextContent):

    def __init__(self, content: Dict = None, text: str = None):
        if content is None:
            # 1. new content with text string
            assert text is not None, 'text should not be None'
            msg_type = ContentType.TEXT
            super().__init__(None, msg_type)
            self['text'] = text
        else:
            # 2. content info from network
            assert text is None, 'params error: %s, %s' % (content, text)
            super().__init__(content)

    #
    #   text
    #
    @property  # Override
    def text(self) -> str:
        return self.get_str(key='text', default='')


class WebPageContent(BaseContent, PageContent):

    def __init__(self, content: Dict = None,
                 url: URI = None, html: str = None, title: str = None,
                 desc: Optional[str] = None, icon: Optional[TransportableFile] = None):
        if content is None:
            # 1. new content with url, title, desc & icon
            assert url is not None and title is not None, 'page info error: %s, %s, %s, %s' % (url, title, desc, icon)
            msg_type = ContentType.PAGE
            super().__init__(None, msg_type)
        else:
            # 2. content info from network
            super().__init__(content)
        self.__icon: Optional[TransportableFile] = None  # PNF
        # URL or HTML
        if url is not None:
            self.url = url
        if html is not None:
            self.html = html
        # title, icon, description
        self.title = title
        if desc is not None:
            self.desc = desc
        if icon is not None:
            self.icon = icon

    # Override
    def to_dict(self) -> Dict:
        # serialize 'icon'
        img = self.__icon
        if img is not None and self.get('icon') is None:
            self['icon'] = img.serialize()
        # OK
        return super().to_dict()

    #
    #   Web Title
    #

    @property  # Override
    def title(self) -> str:
        return self.get_str(key='title', default='')

    @title.setter  # Override
    def title(self, string: str):
        self['title'] = string

    #
    #   Fav Icon
    #

    @property  # Override
    def icon(self) -> Optional[TransportableFile]:
        img = self.__icon
        if img is None:
            base64 = self.get('icon')
            img = TransportableFile.parse(base64)
            self.__icon = img
        return img

    @icon.setter  # Override
    def icon(self, img: TransportableFile):
        self.pop('icon', None)
        # self['icon'] = None if img is None else img.serialize()
        self.__icon = img

    #
    #   Description
    #

    @property  # Override
    def desc(self) -> Optional[str]:
        return self.get_str(key='desc')

    @desc.setter  # Override
    def desc(self, text: Optional[str]):
        if text is None:
            self.pop('desc', None)
        else:
            self['desc'] = text

    #
    #   Page URL
    #

    @property  # Override
    def url(self) -> URI:
        # TODO: convert str to URI
        return self.get_str(key='URL')

    @url.setter  # Override
    def url(self, remote: URI):
        # TODO: convert URI to str
        if remote is None:
            self.pop('URL', None)
        else:
            self['URL'] = remote

    #
    #   Page content
    #

    @property  # Override
    def html(self) -> Optional[str]:
        return self.get_str(key='desc')

    @html.setter  # Override
    def html(self, content: Optional[str]):
        if content is None:
            self.pop('HTML', None)
        else:
            self['HTML'] = content


class NameCardContent(BaseContent, NameCard):

    def __init__(self, content: Dict = None,
                 identifier: ID = None,
                 name: str = None, avatar: Optional[TransportableFile] = None):
        if content is None:
            # 1. new content with ID, name & avatar
            assert identifier is not None and name is not None, \
                'name card info error: %s, %s, %s' % (identifier, name, avatar)
            msg_type = ContentType.NAME_CARD
            super().__init__(None, msg_type)
            # ID
            self.set_string(key='did', value=identifier)
            # name
            self['name'] = name
            # if avatar is not None:
            #     self['avatar'] = avatar.serialize()
        else:
            # 2. content info from network
            assert identifier is None and name is None and avatar is None, \
                'params error: %s, %s, %s, %s' % (content, identifier, name, avatar)
            super().__init__(content=content)
        # lazy load
        self.__avatar = avatar

    # Override
    def to_dict(self) -> Dict:
        # serialize 'avatar'
        img = self.__avatar
        if img is not None and self.get('avatar') is None:
            self['avatar'] = img.serialize()
        # OK
        return super().to_dict()

    @property  # Override
    def identifier(self) -> ID:
        did = self.get('did')
        return ID.parse(identifier=did)

    @property  # Override
    def name(self) -> str:
        return self.get_str(key='name', default='')

    @property  # Override
    def avatar(self) -> Optional[TransportableFile]:
        img = self.__avatar
        if img is None:
            url = self.get('avatar')
            img = TransportableFile.parse(url)
            self.__avatar = img
        return img
