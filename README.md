# Decentralized Instant Messaging Protocol (Python)

[![License](https://img.shields.io/github/license/dimchat/core-py)](https://github.com/dimchat/core-py/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/dimchat/core-py/pulls)
[![Platform](https://img.shields.io/badge/Platform-Python%203-brightgreen.svg)](https://github.com/dimchat/core-py/wiki)
[![Issues](https://img.shields.io/github/issues/dimchat/core-py)](https://github.com/dimchat/core-py/issues)
[![Repo Size](https://img.shields.io/github/repo-size/dimchat/core-py)](https://github.com/dimchat/core-py/archive/refs/heads/master.zip)
[![Tags](https://img.shields.io/github/tag/dimchat/core-py)](https://github.com/dimchat/core-py/tags)
[![Version](https://img.shields.io/pypi/v/dimp)](https://pypi.org/project/dimp)

[![Watchers](https://img.shields.io/github/watchers/dimchat/core-py)](https://github.com/dimchat/core-py/watchers)
[![Forks](https://img.shields.io/github/forks/dimchat/core-py)](https://github.com/dimchat/core-py/forks)
[![Stars](https://img.shields.io/github/stars/dimchat/core-py)](https://github.com/dimchat/core-py/stargazers)
[![Followers](https://img.shields.io/github/followers/dimchat)](https://github.com/orgs/dimchat/followers)

## Dependencies

| Name | Version | Description |
|------|---------|-------------|
| [Ming Ke Ming (名可名)](https://github.com/dimchat/mkm-py) | [![Version](https://img.shields.io/pypi/v/mkm)](https://pypi.org/project/mkm) | Decentralized User Identity Authentication |
| [Dao Ke Dao (道可道)](https://github.com/dimchat/dkd-py) | [![Version](https://img.shields.io/pypi/v/dkd)](https://pypi.org/project/dkd) | Universal Message Module |

## Examples

### Extends Command

* _Handshake Command Protocol_
  0. (C-S) handshake start
  1. (S-C) handshake again with new session
  2. (C-S) handshake restart with new session
  3. (S-C) handshake success

```python
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Optional, Dict

from dimp import Command, BaseCommand


class HandshakeState(IntEnum):
    Start = 0    # C -> S, without session key(or session expired)
    Again = 1    # S -> C, with new session key
    Restart = 2  # C -> S, with new session key
    Success = 3  # S -> C, handshake accepted


def handshake_state(title: str, session: str = None) -> HandshakeState:
    # Server -> Client
    if title == 'DIM!':  # or title == 'OK!':
        return HandshakeState.Success
    if title == 'DIM?':
        return HandshakeState.Again
    # Client -> Server: "Hello world!"
    if session is None or len(session) == 0:
        return HandshakeState.Start
    else:
        return HandshakeState.Restart


class HandshakeCommand(Command, ABC):
    """
        Handshake Command
        ~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x88,
            sn   : 123,

            command : "handshake",    // command name
            title   : "Hello world!", // "DIM?", "DIM!"
            session : "{SESSION_ID}", // session key
        }
    """
    HANDSHAKE = 'handshake'

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def session(self) -> Optional[str]:
        raise NotImplemented

    @property
    @abstractmethod
    def state(self) -> HandshakeState:
        raise NotImplemented

    #
    #   Factories
    #

    @classmethod
    def offer(cls, session: str = None) -> Command:
        """
        Create client-station handshake offer

        :param session: Old session key
        :return: HandshakeCommand object
        """
        return BaseHandshakeCommand(title='Hello world!', session=session)

    @classmethod
    def ask(cls, session: str) -> Command:
        """
        Create station-client handshake again with new session

        :param session: New session key
        :return: HandshakeCommand object
        """
        return BaseHandshakeCommand(title='DIM?', session=session)

    @classmethod
    def accepted(cls, session: str = None) -> Command:
        """
        Create station-client handshake success notice

        :return: HandshakeCommand object
        """
        return BaseHandshakeCommand(title='DIM!', session=session)

    start = offer       # (1. C->S) first handshake, without session
    again = ask         # (2. S->C) ask client to handshake with new session key
    restart = offer     # (3. C->S) handshake with new session key
    success = accepted  # (4. S->C) notice the client that handshake accepted


class BaseHandshakeCommand(BaseCommand, HandshakeCommand):

    def __init__(self, content: Dict = None, title: str = None, session: str = None):
        if content is None:
            # 1. new command with title & session key
            assert title is not None, 'handshake command error: %s' % session
            cmd = self.HANDSHAKE
            super().__init__(cmd=cmd)
            self['title'] = title
            self['message'] = title  # TODO: remove after all clients upgraded
            if session is not None:
                self['session'] = session
        else:
            # 2. command info from network
            assert title is None and session is None, 'params error: %s, %s, %s' % (content, title, session)
            super().__init__(content)

    @property
    def title(self) -> str:
        return self.get_str(key='title', default='')

    @property
    def session(self) -> Optional[str]:
        return self.get_str(key='session')

    @property
    def state(self) -> HandshakeState:
        return handshake_state(title=self.title, session=self.session)
```

### Extends Content

```python
from typing import Any, Dict

from dimp import *


class ApplicationContent(BaseContent, AppContent):
    """
        Application Customized message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0xA0),
            sn   : 123,

            app   : "{APP_ID}",  // application (e.g.: "chat.dim.sechat")
            extra : info         // action parameters
        }
    """

    def __init__(self, content: Dict[str, Any] = None,
                 msg_type: str = None, app: str = None):
        if content is None:
            # 1. new content with type, app_id
            assert app is not None, 'customized content error: %s, %s' % (msg_type, app)
            if msg_type is None:
                msg_type = ContentType.APPLICATION
            super().__init__(None, msg_type)
            self['app'] = app
        else:
            # 2. content info from network
            assert msg_type is None and app is None, 'params error: %s, %s, %s' % (content, msg_type, app)
            super().__init__(content)

    @property  # Override
    def application(self) -> str:
        return self.get_str(key='app', default='')
```

### Extends ID Address

* Examples in [dim plugins](https://pypi.org/project/dimplugins)

----

Copyright &copy; 2018-2025 Albert Moky
[![Followers](https://img.shields.io/github/followers/moky)](https://github.com/moky?tab=followers)
