# -*- coding: utf-8 -*-
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

"""
    Broadcast Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Broadcast information to the whole network (e.g.: User Login Information)
"""

import json

from dkd.utils import base64_encode
from dkd.contents import serial_number

from dkd import MessageType, CommandContent

from mkm import PrivateKey


class BroadcastCommand(CommandContent):
    """
        Broadcast Command
        ~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command     : "broadcast", // command name
            information : {...},       // broadcast information
            traces      : [...],       // broadcast traces
        }
    """

    #
    #   broadcast information
    #
    @property
    def information(self) -> dict:
        return self.get('information')

    @information.setter
    def information(self, value: dict):
        if value:
            self['information'] = value
        else:
            self.pop('information')

    #
    #   broadcast traces
    #
    @property
    def traces(self) -> list:
        return self.get('traces')

    @traces.setter
    def traces(self, value):
        if value:
            self['traces'] = value
        else:
            self.pop('traces')

    #
    #   Factories
    #
    @classmethod
    def broadcast(cls, information: dict, traces: list =None) -> CommandContent:
        """
        Create broadcast command for information with traces

        :param information: Dictionary to broadcast
        :param traces: The stations on the way
        :return: BroadcastCommand object
        """
        content = {
            'type': MessageType.Command,
            'sn': serial_number(),
            'command': 'broadcast',
            'information': information,
        }
        if traces:
            content['traces'] = traces
        return BroadcastCommand(content)

    @classmethod
    def login(cls, account: str, private_key: PrivateKey,
              host: str, port: int =9394, time: int =0) -> CommandContent:
        """
        Create broadcast command for login connection

        :param account: Login account ID
        :param private_key: Login account's private key to sign the connection info
        :param host: Login station's IP
        :param port: Login station's port
        :param time: Login time
        :return: BroadcastCommand object
        """
        connection = {
            # 'station': 'STATION_ID',
            'host': host,
            'port': port,
            'time': time,

            'account': account,
            # 'terminal': 'DEVICE_ID',
            # 'user_agent': 'USER_AGENT',
        }
        data = json.dumps(connection).encode('utf-8')
        signature = private_key.sign(data)
        info = {
            'login': data,
            'signature': base64_encode(signature),
        }
        return cls.broadcast(information=info)
