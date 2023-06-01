# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2022 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2022 Albert Moky
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

from mkm.types import Wrapper

from dkd.factory import MessageFactoryManager

from ..protocol import Command, CommandFactory


class CommandGeneralFactory:

    def __init__(self):
        super().__init__()
        self.__command_factories: Dict[str, CommandFactory] = {}

    def set_command_factory(self, cmd: str, factory: CommandFactory):
        self.__command_factories[cmd] = factory

    def get_command_factory(self, cmd: str) -> Optional[CommandFactory]:
        return self.__command_factories.get(cmd)

    # noinspection PyMethodMayBeStatic
    def get_cmd(self, content: Dict[str, Any]) -> Optional[str]:
        return content.get('command')

    def parse_command(self, content: Any) -> Optional[Command]:
        if content is None:
            return None
        elif isinstance(content, Command):
            return content
        info = Wrapper.get_dict(content)
        if info is None:
            # assert False, 'command content error: %s' % content
            return None
        # get factory by command name
        cmd = self.get_cmd(content=info)
        factory = None if cmd is None else self.get_command_factory(cmd=cmd)
        if factory is None:
            # unknown command name, get base command factory
            gf = MessageFactoryManager.general_factory
            msg_type = gf.get_content_type(content=info)
            assert msg_type is not None, 'content type not found: %s' % info
            fact = gf.get_content_factory(msg_type=msg_type)
            if isinstance(fact, CommandFactory):
                factory = fact
            else:
                assert False, 'cannot parse command: %s' % info
        return factory.parse_command(content=info)


# Singleton
class CommandFactoryManager:

    general_factory = CommandGeneralFactory()
