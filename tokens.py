from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.account import get_balance
from xrpl.utils import xrp_to_drops, drops_to_xrp
from xrpl.models.transactions import AccountSet, TrustSet, AMMCreate
from xrpl.models.transactions.account_set import AccountSetAsfFlag
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.transaction import submit_and_wait

def convert_string_to_hex_padded(s):
    hex_str = s.encode().hex()
    return hex_str.ljust(40, "0").upper()


def tokens():
    print("Let's manage tokens... 📊")
