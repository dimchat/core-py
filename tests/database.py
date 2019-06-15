# -*- coding: utf-8 -*-

from dimp import *


class Facebook(IBarrackDelegate):

    #
    #   IBarrackDelegate
    #
    def account(self, identifier: ID) -> Account:
        # TODO: create account
        entity = Account(identifier=identifier)
        entity.delegate = barrack
        return entity

    def user(self, identifier: ID) -> User:
        # TODO: create user
        entity = User(identifier=identifier)
        entity.delegate = barrack
        return entity

    def group(self, identifier: ID) -> Group:
        # TODO: create group
        entity = Group(identifier=identifier)
        entity.delegate = barrack
        return entity


class Database(IUserDataSource, IGroupDataSource, ITransceiverDataSource):

    def __init__(self):
        super().__init__()
        # memory cache
        self.__private_keys = {}

    def cache_private_key(self, private_key: PrivateKey, identifier: ID):
        self.__private_keys[identifier.address] = private_key

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
        return facebook.account(identifier=identifier)

    def user(self, identifier: ID) -> User:
        return facebook.user(identifier=identifier)

    def group(self, identifier: ID) -> Group:
        return facebook.group(identifier=identifier)

    #
    #   ITransceiverDataSource
    #
    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        # TODO: save meta to local storage
        pass

    def cipher_key(self, sender: ID, receiver: ID) -> SymmetricKey:
        return keystore.cipher_key(sender=sender, receiver=receiver)

    def cache_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID) -> bool:
        return keystore.cache_cipher_key(key=key, sender=sender, receiver=receiver)

    def reuse_cipher_key(self, sender: ID, receiver: ID, key: SymmetricKey) -> SymmetricKey:
        pass


database = Database()

facebook = Facebook()

keystore = KeyStore()

barrack = Barrack()
barrack.entityDataSource = database
barrack.userDataSource = database
barrack.groupDataSource = database
barrack.delegate = database

transceiver = Transceiver()
transceiver.dataSource = database
transceiver.delegate = facebook
