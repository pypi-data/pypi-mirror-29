from decimal import Decimal
from typing import List, Tuple

import requests

from cryptoportfolio.interfaces.base import CryptoCoinWallet


class EmercoinWallet(CryptoCoinWallet):
    decimal_places = 18

    def _get_addr_coins_and_tokens_balance(self) -> List[Tuple[str, Decimal]]:
        data = requests.get(
            "https://emercoin.mintr.org/api/address/balance/%s" % self.addr
        ).json()
        return [
            ("EMC", Decimal(data['balance'])),
        ]
