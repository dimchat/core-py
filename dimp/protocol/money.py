# -*- coding: utf-8 -*-
#
#   DIMP : Decentralized Instant Messaging Protocol
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
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

from abc import ABC
from typing import Optional

from mkm import ID
from dkd import Content


class MoneyContent(Content, ABC):
    """
        Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x40,
            sn   : 123,

            currency : "RMB", // USD, USDT, ...
            amount   : 100.00
        }
    """

    @property
    def currency(self) -> str:
        raise NotImplemented

    @property
    def amount(self) -> float:
        raise NotImplemented

    @amount.setter
    def amount(self, value: float):
        raise NotImplemented


class TransferContent(MoneyContent, ABC):
    """
        Transfer Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x41,
            sn   : 123,

            currency : "RMB",    // USD, USDT, ...
            amount   : 100.00,
            remitter : "{FROM}", // sender ID
            remittee : "{TO}"    // receiver ID
        }
    """

    @property
    def remitter(self) -> Optional[ID]:
        raise NotImplemented

    @remitter.setter
    def remitter(self, sender: Optional[ID]):
        raise NotImplemented

    @property
    def remittee(self) -> Optional[ID]:
        raise NotImplemented

    @remittee.setter
    def remittee(self, receiver: Optional[ID]):
        raise NotImplemented