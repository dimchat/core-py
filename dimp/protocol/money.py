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

from abc import ABC, abstractmethod
from typing import Optional

from mkm import ID
from dkd import Content

from .types import ContentType


class MoneyContent(Content, ABC):
    """
        Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x40),
            sn   : 123,

            currency : "RMB", // USD, USDT, ...
            amount   : 100.00
        }
    """

    @property
    @abstractmethod
    def currency(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def amount(self) -> float:
        raise NotImplemented

    @amount.setter
    @abstractmethod
    def amount(self, value: float):
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def create(cls, currency: str, amount: float, msg_type: str = None):
        # convert type value
        if msg_type is None:
            msg_type = ContentType.MONEY
        # create with type value
        from ..dkd import BaseMoneyContent
        return BaseMoneyContent(msg_type=msg_type, currency=currency, amount=amount)


class TransferContent(MoneyContent, ABC):
    """
        Transfer Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : i2s(0x41),
            sn   : 123,

            currency : "RMB",    // USD, USDT, ...
            amount   : 100.00,
            remitter : "{FROM}", // sender ID
            remittee : "{TO}"    // receiver ID
        }
    """

    @property
    @abstractmethod
    def remitter(self) -> Optional[ID]:
        raise NotImplemented

    @remitter.setter
    @abstractmethod
    def remitter(self, sender: ID):
        raise NotImplemented

    @property
    @abstractmethod
    def remittee(self) -> Optional[ID]:
        raise NotImplemented

    @remittee.setter
    @abstractmethod
    def remittee(self, receiver: ID):
        raise NotImplemented

    #
    #   Factory method
    #
    @classmethod
    def transfer(cls, currency: str, amount: float):
        from ..dkd import TransferMoneyContent
        return TransferMoneyContent(currency=currency, amount=amount)
