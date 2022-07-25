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

from typing import Optional, Union, Any, Dict

from dkd import ContentType, BaseContent

from ..protocol import Command


class BaseCommand(BaseContent, Command):

    def __init__(self, content: Optional[Dict[str, Any]] = None,
                 msg_type: Union[int, ContentType] = 0,
                 cmd: Optional[str] = None):
        if content is None and msg_type == 0:
            msg_type = ContentType.COMMAND
        super().__init__(content=content, msg_type=msg_type)
        if cmd is not None:
            # TODO: modify after all server/clients support 'cmd'
            # self['cmd'] = cmd
            self['command'] = cmd

    @property  # Override
    def cmd(self) -> str:
        return command_name(content=self.dictionary)


def command_name(content: Dict[str, Any]) -> str:
    # TODO: modify after all server/clients support 'cmd'
    cmd = content.get('cmd')
    if cmd is None:
        cmd = content.get('command')
    return cmd
