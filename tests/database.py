# -*- coding: utf-8 -*-

from dimp import *


class Facebook(Barrack):

    def __init__(self):
        super().__init__()
        # memory cache
        self.__private_keys = {}

    def cache_private_key(self, private_key: PrivateKey, identifier: ID):
        self.__private_keys[identifier.address] = private_key

    #
    #   IBarrackDelegate
    #
    def account(self, identifier: ID) -> Account:
        entity = super().account(identifier=identifier)
        if entity is None:
            entity = super().user(identifier=identifier)
            if entity is None:
                entity = Account(identifier=identifier)
                self.cache_account(account=entity)
        return entity

    def user(self, identifier: ID) -> User:
        entity = super().user(identifier=identifier)
        if entity is None:
            entity = User(identifier=identifier)
            self.cache_user(user=entity)
        return entity

    def group(self, identifier: ID) -> Group:
        entity = super().group(identifier=identifier)
        if entity is None:
            entity = Group(identifier=identifier)
            self.cache_group(group=entity)
        return entity

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


class KeyStore(KeyCache):

    def save_keys(self, key_map: dict) -> bool:
        return False

    def load_keys(self) -> dict:
        pass

    def reuse_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID) -> SymmetricKey:
        pass


facebook = Facebook()

keystore = KeyStore()

transceiver = Transceiver()
transceiver.barrack = facebook
transceiver.key_cache = keystore
