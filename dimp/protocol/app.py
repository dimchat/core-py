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
from typing import Dict

from dkd import Content

from .types import ContentType
from .base import BaseContent


class AppContent(Content, ABC):
    """
        Content for Application 0nly
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0xA0),
            sn   : 123,

            app   : "{APP_ID}",  // application (e.g.: "chat.dim.sechat")
            extra : info         // action parameters
        }
    """

    @property
    @abstractmethod
    def application(self) -> str:
        """ App ID """
        raise NotImplemented


class CustomizedContent(AppContent, ABC):
    """
        Application Customized message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0xCC),
            sn   : 123,

            app   : "{APP_ID}",  // application (e.g.: "chat.dim.sechat")
            mod   : "{MODULE}",  // module name (e.g.: "drift_bottle")
            act   : "{ACTION}",  // action name (e.g.: "throw")
            extra : info         // action parameters
        }
    """

    @property
    @abstractmethod
    def module(self) -> str:
        """ Module Name """
        raise NotImplemented

    @property
    @abstractmethod
    def action(self) -> str:
        """ Action Name """
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, app: str, mod: str, act: str):
        return AppCustomizedContent(app=app, mod=mod, act=act)


###############################
#                             #
#   DaoKeDao Implementation   #
#                             #
###############################


class AppCustomizedContent(BaseContent, CustomizedContent):

    def __init__(self, content: Dict = None,
                 msg_type: str = None,
                 app: str = None, mod: str = None, act: str = None):
        if content is None:
            # 1. new content with type, application, module & action
            assert app is not None and mod is not None and act is not None, \
                'customized content error: %s, %s, %s, %s' % (msg_type, app, mod, act)
            if msg_type is None:
                msg_type = ContentType.CUSTOMIZED
            super().__init__(None, msg_type)
            self['app'] = app
            self['mod'] = mod
            self['act'] = act
        else:
            # 2. content info from network
            assert msg_type is None and app is None and mod is None and act is None, \
                'params error: %s, %s, %s, %s, %s' % (content, msg_type, app, mod, act)
            super().__init__(content)

    @property  # Override
    def application(self) -> str:
        return self.get_str(key='app', default='')

    @property  # Override
    def module(self) -> str:
        return self.get_str(key='mod', default='')

    @property  # Override
    def action(self) -> str:
        return self.get_str(key='act', default='')
