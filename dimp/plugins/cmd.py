# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2024 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2024 Albert Moky
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

from mkm.types import Singleton

from ..protocol.commands import CommandHelper
from ..protocol.helpers import CommandExtensions


# class GeneralCommandHelper(CommandHelper, ABC):
class GeneralCommandHelper(ABC):
    """ Command GeneralFactory """

    #
    #   CMD - Command, Method, Declaration
    #

    @abstractmethod
    def get_cmd(self, content: Dict, default: Optional[str]) -> Optional[str]:
        raise NotImplemented


@Singleton
class SharedCommandExtensions:
    """ Command FactoryManager """

    def __init__(self):
        super().__init__()
        self.__helper: Optional[GeneralCommandHelper] = None

    @property
    def helper(self) -> Optional[GeneralCommandHelper]:
        return self.__helper

    @helper.setter
    def helper(self, helper: GeneralCommandHelper):
        self.__helper = helper

    #
    #   Command
    #

    @property
    def cmd_helper(self) -> Optional[CommandHelper]:
        return CommandExtensions.cmd_helper

    @cmd_helper.setter
    def cmd_helper(self, helper: CommandHelper):
        CommandExtensions.cmd_helper = helper
