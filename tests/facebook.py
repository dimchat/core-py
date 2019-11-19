# -*- coding: utf-8 -*-

from typing import Optional

from mkm.immortals import Immortals

from dimp import NetworkID, ID, Meta, Profile, Group
from dimp import Barrack, User, PrivateKey


class Facebook(Barrack):

    def __init__(self):
        super().__init__()
        self.__immortals = Immortals()

    def nickname(self, identifier: ID) -> str:
        assert identifier.type.is_user(), 'ID error: %s' % identifier
        user = self.user(identifier=identifier)
        if user is not None:
            return user.name

    def verify_profile(self, profile: Profile) -> bool:
        if profile is None:
            return False
        elif profile.valid:
            # already verified
            return True
        # try to verify the profile
        identifier = self.identifier(profile.identifier)
        if identifier.type.is_user() or identifier.type.value == NetworkID.Polylogue:
            # if this is a user profile,
            #     verify it with the user's meta.key
            # else if this is a polylogue profile,
            #     verify it with the founder's meta.key (which equals to the group's meta.key)
            meta = self.meta(identifier=identifier)
            if meta is not None:
                return profile.verify(public_key=meta.key)
        else:
            raise NotImplementedError('unsupported profile ID: %s' % profile)

    @staticmethod
    def verify_meta(meta: Meta, identifier: ID) -> bool:
        if meta is not None:
            return meta.match_identifier(identifier)

    def save_meta(self, meta: Meta, identifier: ID) -> bool:
        # TODO: save meta into local storage
        pass

    #
    #   SocialNetworkDataSource
    #
    def identifier(self, string: str) -> Optional[ID]:
        # get from barrack
        return super().identifier(string=string)

    def user(self, identifier: ID) -> Optional[User]:
        #  get from barrack cache
        user = super().user(identifier=identifier)
        if user is not None:
            return user
        # check meta and private key
        meta = self.meta(identifier=identifier)
        if meta is not None:
            user = User(identifier=identifier)
            # cache it in barrack
            self.cache_user(user=user)
            return user

    def group(self, identifier: ID) -> Optional[Group]:
        # get from barrack cache
        group = super().group(identifier=identifier)
        if group is not None:
            return group
        # check meta
        meta = self.meta(identifier=identifier)
        if meta is not None:
            group = Group(identifier=identifier)
            # cache it in barrack
            self.cache_group(group=group)
            return group

    #
    #   EntityDataSource
    #
    def meta(self, identifier: ID) -> Optional[Meta]:
        info = super().meta(identifier=identifier)
        if info is not None:
            return info
        return self.__immortals.meta(identifier=identifier)
        # TODO: load meta from database

    def profile(self, identifier: ID) -> Optional[Profile]:
        return self.__immortals.profile(identifier=identifier)
        # TODO: load profile from database

    #
    #   UserDataSource
    #
    def contacts(self, identifier: ID) -> Optional[list]:
        array = super().contacts(identifier=identifier)
        if array is not None:
            return array
        # TODO: load contacts from database

    def private_keys_for_decryption(self, identifier: ID) -> Optional[list]:
        return self.__immortals.private_keys_for_decryption(identifier=identifier)
        # TODO: load private keys from local storage

    def private_key_for_signature(self, identifier: ID) -> Optional[PrivateKey]:
        return self.__immortals.private_key_for_signature(identifier=identifier)
        # TODO: load private key from local storage

    #
    #   GroupDataSource
    #
    def founder(self, identifier: ID) -> Optional[ID]:
        return super().founder(identifier=identifier)

    def owner(self, identifier: ID) -> ID:
        return super().owner(identifier=identifier)

    def members(self, identifier: ID) -> Optional[list]:
        return super().members(identifier=identifier)
