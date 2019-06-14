# -*- coding: utf-8 -*-

from dimp import *
from dimp.barrack import barrack


class Database(IUserDataSource, IGroupDataSource, IBarrackDelegate):

    def __init__(self):
        super().__init__()
        # memory cache
        self.__private_keys = {}

    def cache_private_key(self, private_key: PrivateKey, identifier: ID):
        self.__private_keys[identifier.address] = private_key

    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        # TODO: save meta to local storage
        pass


    #
    #   IEntityDataSource
    #
    def meta(self, identifier: ID) -> Meta:
        # TODO: load meta from local storage
        pass

    def profile(self, identifier: ID) -> Profile:
        # TODO: load profile from local storage
        pass

    #
    #   IUserDataSource
    #
    def private_key_for_signature(self, identifier: ID) -> PrivateKey:
        # TODO: load private key from keychain
        return self.__private_keys.get(identifier.address)

    def private_keys_for_decryption(self, identifier: ID) -> list:
        # TODO: load private key from keychain
        key = self.__private_keys.get(identifier.address)
        return [key]

    def contacts(self, identifier: ID) -> list:
        # TODO: load contacts from local storage
        pass

    #
    #   IGroupDataSource
    #
    def founder(self, identifier: ID) -> ID:
        # TODO: load group info from local storage
        pass

    def owner(self, identifier: ID) -> ID:
        # TODO: load group info from local storage
        pass

    def members(self, identifier: ID) -> list:
        # TODO: load group info from local storage
        pass

    #
    #   IBarrackDelegate
    #

    def account(self, identifier: ID) -> Account:
        # TODO: create account
        pass

    def user(self, identifier: ID) -> User:
        # TODO: create user
        pass

    def group(self, identifier: ID) -> Group:
        # TODO: create group
        pass


database = Database()
barrack.entityDataSource = database
barrack.userDataSource = database
barrack.groupDataSource = database
barrack.delegate = database
