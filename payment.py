from re import sub
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.account import get_balance
from xrpl.utils import xrp_to_drops, drops_to_xrp
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait

def payment():
    client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

    # Create wallets and fund them
    sender_wallet = generate_faucet_wallet(client)
    receiver_wallet = generate_faucet_wallet(client)

    # Fetch balances
    sender_balance = get_balance(sender_wallet.address, client)
    receiver_balance = get_balance(receiver_wallet.address, client)

    # Display sender info
    print(f"Sender Address: {sender_wallet.classic_address}")
    print(f"Sender Balance: {drops_to_xrp(str(sender_balance))} XRP")

    # Display receiver info
    print(f"Receiver Address: {receiver_wallet.classic_address}")
    print(f"Receiver Balance: {drops_to_xrp(str(receiver_balance))} XRP")

    # Prepare the transaction
    payment_tx = Payment(
        account=sender_wallet.address,
        destination=receiver_wallet.address,
        amount=xrp_to_drops(10)
    )

    # Sign and submit the transaction
    payment_result = submit_and_wait(payment_tx, client, sender_wallet, autofill=True)

    # Verify the result
    if payment_result.is_successful():
        print("✅ Payment tx succeeded: ", payment_result.result['hash'])
    else:
        print("❌ Payment tx failed: ", payment_result.result)