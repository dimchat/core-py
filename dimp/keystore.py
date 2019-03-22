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
    Symmetric Keys Storage
    ~~~~~~~~~~~~~~~~~~~~~~

    Manage keys for conversations
"""

from mkm import ID, SymmetricKey


class KeyStore:

    def __init__(self):
        super().__init__()
        # current user
        self.user = None

        # memory cache
        self.key_table = {}
        self.dirty = False

    def cipher_key(self, sender: ID, receiver: ID) -> SymmetricKey:
        key_map = self.key_table.get(sender.address)
        if key_map:
            return key_map.get(receiver.address)

    def cache_cipher_key(self, key: SymmetricKey, sender: ID, receiver: ID) -> bool:
        key_map = self.key_table.get(sender.address)
        if key_map is None:
            key_map = {}
            self.key_table[sender.address] = key_map
        if key:
            key_map[receiver.address] = key
            self.dirty = True
            return True
        else:
            raise ValueError('cipher key cannot be empty')

    def flush(self):
        if self.dirty:
            # write key table to persistent storage
            pass

    def reload(self):
        # load key table from persistent storage
        pass
