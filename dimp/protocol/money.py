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

from typing import Optional, Union

from dkd import ContentType, BaseContent


class MoneyContent(BaseContent):
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

    def __init__(self, content: Optional[dict] = None, content_type: Union[ContentType, int] = 0,
                 currency: Optional[str] = None, amount: Optional[float] = 0.0):
        if content is None:
            if content_type == 0:
                content_type = ContentType.MONEY
            super().__init__(content_type=content_type)
        else:
            super().__init__(content=content)
        # set values to inner dictionary
        if currency is not None:
            self['currency'] = currency
        if amount > 0:
            self['amount'] = amount

    @property
    def currency(self) -> str:
        return self.get('currency')

    @property
    def amount(self) -> float:
        return float(self.get('amount'))

    @amount.setter
    def amount(self, value: float):
        self['amount'] = value


class TransferContent(MoneyContent):
    """
        Transfer Money Message Content
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            type : 0x41,
            sn   : 123,

            currency : "RMB", // USD, USDT, ...
            amount   : 100.00
        }
    """

    def __init__(self, content: Optional[dict] = None, currency: Optional[str] = None, amount: Optional[float] = 0.0):
        super().__init__(content, ContentType.TRANSFER, currency=currency, amount=amount)
