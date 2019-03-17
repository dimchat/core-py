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


class KeyStore:

    def __init__(self):
        super().__init__()
        # current user
        self.user = None

        # memory cache
        self.keys_for_accounts = {}
        self.keys_from_accounts = {}
        self.keys_for_groups = {}
        self.tables_from_groups = {}

    def cipher_key(self, sender: str=None, receiver: str=None, group: str=None) -> dict:
        if group is None:
            # personal message
            if sender:
                # cipher key from contact
                return self.keys_from_accounts.get(sender)
            elif receiver:
                # cipher key for contact
                return self.keys_for_accounts.get(receiver)
        else:
            # group message
            if sender:
                # cipher key from group member(sender)
                table = self.tables_from_groups.get(group)
                if table:
                    return table.get(sender)
            else:
                # cipher key for group
                return self.keys_for_groups.get(group)

    def retain_cipher_key(self, key: dict, sender: str=None, receiver: str=None, group: str=None):
        if group is None:
            # personal message
            if sender:
                # cipher key from contact
                self.keys_from_accounts[sender] = key
            elif receiver:
                # cipher key for contact
                self.keys_for_accounts[receiver] = key
        else:
            # group message
            if sender:
                # cipher key from group member(sender)
                table = self.tables_from_groups.get(group)
                if table:
                    table[sender] = key
                else:
                    table = {sender: key}
                self.tables_from_groups[group] = table
            else:
                # cipher key for group
                self.keys_for_groups[group] = key
