# -*- coding: utf-8 -*-

import os
from typing import Optional

from mkm.dos import JSONFile

from dimp import User
from dimp import KeyCache


class KeyStore(KeyCache):

    def __init__(self):
        super().__init__()
        self.__user: User = None
        self.__base_dir: str = '/tmp/.dim/'

    @property
    def user(self) -> Optional[User]:
        return self.__user

    @user.setter
    def user(self, value: User):
        if value is None:
            # save key map for old user
            self.flush()
            self.__user = None
        elif value != self.__user:
            # load key map for new user
            self.__user = value
            self.update_keys(self.load_keys())

    @property
    def directory(self) -> str:
        return self.__base_dir

    @directory.setter
    def directory(self, value: str):
        self.__base_dir = value

    # '/tmp/.dim/protected/{ADDRESS}/keystore.js'
    def __path(self) -> Optional[str]:
        if self.__user is None:
            return None
        return os.path.join(self.__base_dir, 'protected', self.__user.identifier, 'keystore.js')

    def save_keys(self, key_map: dict) -> bool:
        # write key table to persistent storage
        path = self.__path()
        if path is None:
            return False
        return JSONFile(path).write(key_map)

    def load_keys(self) -> Optional[dict]:
        # load key table from persistent storage
        path = self.__path()
        if path is None:
            return None
        return JSONFile(path).read()
