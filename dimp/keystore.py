# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
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
    Symmetric Keys Storage
    ~~~~~~~~~~~~~~~~~~~~~~

    Manage keys for conversations
"""

from mkm import SymmetricKey, ID, Address
from mkm.address import ANYWHERE, EVERYWHERE
from mkm.crypto.symmetric import symmetric_key_classes

from .delegate import ICipherKeyDataSource


class PlainKey(SymmetricKey):
    """
        Symmetric key for broadcast message,
        which will do nothing when en/decoding message data
    """

    PLAIN = 'PLAIN'

    def encrypt(self, data: bytes) -> bytes:
        return data

    def decrypt(self, data: bytes) -> bytes:
        return data


symmetric_key_classes[PlainKey.PLAIN] = PlainKey
plain_key = PlainKey({'algorithm': PlainKey.PLAIN})


def is_broadcast(to: Address) -> bool:
    network = to.network
    if network.is_person():
        return to == ANYWHERE
    elif network.is_group():
        return to == EVERYWHERE


class KeyStore(ICipherKeyDataSource):

    def __init__(self):
        super().__init__()
        # memory cache
        self.key_map = {}
        self.dirty = False
        # load keys from local storage
        self.update_keys(self.load_keys())

    def flush(self):
        """ Trigger for saving cipher key table """
        if self.dirty:
            if self.save_keys(self.key_map):
                # keys saved
                self.dirty = False

    def save_keys(self, key_map: dict) -> bool:
        """
        Callback for saving cipher key table into local storage

        :param key_map: all cipher keys(with direction) from memory cache
        :return:        True on success
        """
        # TODO: Override it to access database
        pass

    def load_keys(self) -> dict:
        """
        Load cipher key table from local storage

        :return: keys map
        """
        # TODO: Override it to access database
        pass

    def update_keys(self, key_map: dict) -> bool:
        """
        Update cipher key table into memory cache

        :param key_map: cipher keys(with direction) from local storage
        :return:        False on nothing changed
        """
        if key_map is None:
            return False
        changed = False
        for _from in key_map:
            table = key_map.get(_from)
            for _to in table:
                pw = table.get(_to)
                key = SymmetricKey(pw)
                # TODO: check whether exists an old key
                changed = True
                # cache key with direction
                self._cache_cipher_key(key, _from, _to)
        return changed

    def _cipher_key(self, _from: Address, _to: Address) -> SymmetricKey:
        if is_broadcast(_to):
            return plain_key
        table = self.key_map.get(_from)
        if table is not None:
            return table.get(_to)

    def _cache_cipher_key(self, key: SymmetricKey, _from: Address, _to: Address) -> bool:
        if is_broadcast(_to):
            return True
        table = self.key_map.get(_from)
        if table is None:
            table = {}
            self.key_map[_from] = table
        if key is not None:
            table[_to] = key
            return True

    #
    #   ICipherKeyDataSource
    #
    def cipher_key(self, sender: ID, receiver: ID) -> SymmetricKey:
        return self._cipher_key(sender.address, receiver.address)

    def cache_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID) -> bool:
        if self._cache_cipher_key(key, sender.address, receiver.address):
            self.dirty = True

    def reuse_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID) -> SymmetricKey:
        # TODO: check reuse key
        pass
