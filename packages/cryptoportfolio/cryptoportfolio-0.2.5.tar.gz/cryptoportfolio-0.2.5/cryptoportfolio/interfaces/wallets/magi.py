from decimal import Decimal
from typing import List, Tuple

import requests

from cryptoportfolio.interfaces.base import CryptoCoinWallet


class MagiWallet(CryptoCoinWallet):
    decimal_places = 18

    def _get_addr_coins_and_tokens_balance(self) -> List[Tuple[str, Decimal]]:
        balance = requests.get(
            "https://chainz.cryptoid.info/xmg/api.dws?q=getbalance&a=%s" % self.addr
        ).text
        return [
            ("XMG", Decimal(balance))
        ]
