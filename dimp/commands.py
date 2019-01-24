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
    Commands
    ~~~~~~~~

    Extents Commands for Message Content
"""

from mkm.utils import base64_encode

from dkd.transform import json_str
from dkd.contents import serial_number

from dkd import PrivateKey
from dkd import ID, Meta

from dkd import MessageType, CommandContent


"""
    Handshake Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    1. (C-S) handshake start
    2. (S-C) handshake again with new session
    3. (C-S) handshake start with new session
    4. (S-C) handshake success
"""


def handshake_command(message: str='', session: object=None) -> CommandContent:
    content = {
        'type': MessageType.Command,
        'sn': serial_number(),
        'command': 'handshake',
        'message': message,
    }
    if session:
        content['session'] = session
    return CommandContent(content)


def handshake_start_command(session: object=None) -> CommandContent:
    """
    Create client-station handshake start

    :param session: Old session ID
    :return:
    """
    return handshake_command(message='Hello world!', session=session)


def handshake_again_command(session: object) -> CommandContent:
    """
    Create station-client handshake again with new session

    :param session: New session ID
    :return:
    """
    return handshake_command(message='DIM?', session=session)


def handshake_success_command() -> CommandContent:
    """
    Create station-client handshake success notice

    :return:
    """
    return handshake_command(message='DIM!')


"""
    Group Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~
    
    1. invite member
    2. expel member
    3. member quit
"""


def group_command(group: ID, command: str, member: ID=None) -> CommandContent:
    content = {
        'type': MessageType.Command,
        'sn': serial_number(),
        'command': command,
        'group': group,
    }
    if member:
        content['member'] = member
    return CommandContent(content)


def invite_command(group: ID, member: ID) -> CommandContent:
    """
    Create invite member command

    :param group:  Group ID
    :param member: User ID
    :return:
    """
    return group_command(group=group, command='invite', member=member)


def expel_command(group: ID, member: ID) -> CommandContent:
    """
    Create expel member command

    :param group:  Group ID
    :param member: Member ID
    :return:
    """
    return group_command(group=group, command='expel', member=member)


def quit_command(group: ID, member: ID) -> CommandContent:
    """
    Create member quit command

    :param group:  Group ID
    :param member: Member ID
    :return:
    """
    return group_command(group=group, command='quit', member=member)


"""
    Broadcast Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Broadcast information to the whole network (e.g.: User Login Information)
"""


def broadcast_command(broadcast: dict) -> CommandContent:
    content = {
        'type': MessageType.Command,
        'sn': serial_number(),
        'command': 'broadcast',
        'broadcast': broadcast,
        'traces': [],
    }
    return CommandContent(content)


def login_command(account: ID, private_key: PrivateKey,
                  host: str, port: int=9394, time: int=0) -> CommandContent:
    login = {
        # 'station': 'STATION_ID',
        'host': host,
        'port': port,
        'time': time,

        'account': account,
        # 'terminal': 'DEVICE_ID',
        # 'user_agent': 'USER_AGENT',
    }
    info = json_str(login).encode('utf-8')
    signature = private_key.sign(info)
    broadcast = {
        'login': info,
        'signature': base64_encode(signature),
    }
    return broadcast_command(broadcast=broadcast)


"""
    Meta Command Protocol
    ~~~~~~~~~~~~~~~~~~~~~
    
    1. contains 'identifier' only, means query meta for ID
    2. contains 'meta' (must match), means reply
"""


def meta_command(identifier: ID, meta: Meta=None) -> CommandContent:
    content = {
        'type': MessageType.Command,
        'sn': serial_number(),
        'command': 'meta',
        'identifier': identifier,
    }
    if meta:  # and meta.match_identifier(identifier):
        content['meta'] = meta
    return CommandContent(content)
