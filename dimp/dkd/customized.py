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

from typing import Any, Dict

from dkd import ContentType

from ..protocol import CustomizedContent

from .base import BaseContent


class AppCustomizedContent(BaseContent, CustomizedContent):
    """
        Application Customized message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0xCC,
            sn   : 123,

            app   : "{APP_ID}",  // application (e.g.: "chat.dim.sechat")
            mod   : "{MODULE}",  // module name (e.g.: "drift_bottle")
            act   : "{ACTION}",  // action name (e.g.: "throw")
            extra : info         // action parameters
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 msg_type: int = None,
                 app: str = None, mod: str = None, act: str = None):
        if content is None:
            # 1. new content with type, application, module & action
            assert app is not None and mod is not None and act is not None, \
                'customized content error: %s, %s, %s, %s' % (msg_type, app, mod, act)
            if msg_type is None:
                msg_type = ContentType.CUSTOMIZED.value
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
