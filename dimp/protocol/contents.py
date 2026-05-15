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
        """ Get text """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.text getter'
        )

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
        """ Get title """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.title getter'
        )

    @title.setter
    @abstractmethod
    def title(self, string: str):
        """ Set title """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.title setter'
        )

    #
    #   Fav Icon
    #

    @property
    @abstractmethod
    def icon(self) -> Optional[TransportableFile]:
        """ Get icon """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.icon getter'
        )

    @icon.setter
    @abstractmethod
    def icon(self, img: TransportableFile):
        """ Set icon """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.icon setter'
        )

    #
    #   Description
    #

    @property
    @abstractmethod
    def desc(self) -> Optional[str]:
        """ Get description """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.desc getter'
        )

    @desc.setter
    @abstractmethod
    def desc(self, text: str):
        """ Set description """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.desc setter'
        )

    #
    #   Page URL
    #

    @property
    @abstractmethod
    def url(self) -> Optional[URI]:
        """ Get URL """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.url getter'
        )

    @url.setter
    @abstractmethod
    def url(self, locator: URI):
        """ Set URL """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.url setter'
        )

    #
    #   Page content
    #

    @property
    @abstractmethod
    def html(self) -> Optional[str]:
        """ Get HTML """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.html getter'
        )

    @html.setter
    @abstractmethod
    def html(self, content: str):
        """ Set HTML """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.html setter'
        )

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
        """ Get did """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.identifier getter'
        )

    @property
    @abstractmethod
    def name(self) -> str:
        """ Get name """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.name getter'
        )

    @property
    @abstractmethod
    def avatar(self) -> Optional[TransportableFile]:
        """ Get avatar """
        raise NotImplementedError(
            f'Not implemented: {type(self).__module__}.{type(self).__name__}.avatar getter'
        )

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
            assert text is None, f'params error: {content}, {text}'
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
            assert url is not None and title is not None, f'page info error: {url}, {title}, {desc}, {icon}'
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
                f'name card info error: {identifier}, {name}, {avatar}'
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
                f'params error: {content}, {identifier}, {name}, {avatar}'
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
