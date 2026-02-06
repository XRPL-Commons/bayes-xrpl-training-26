from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.account import get_balance
from xrpl.utils import xrp_to_drops, drops_to_xrp
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait

def payment():
    print("Let's make payments... 💰")