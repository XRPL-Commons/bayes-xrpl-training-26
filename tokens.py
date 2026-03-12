from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.account import get_balance
from xrpl.utils import xrp_to_drops, drops_to_xrp
from xrpl.models.transactions import AccountSet, TrustSet, AMMCreate, Payment
from xrpl.models.transactions.account_set import AccountSetAsfFlag
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.transaction import submit_and_wait

def convert_string_to_hex_padded(s):
    hex_str = s.encode().hex()
    return hex_str.ljust(40, "0").upper()

def tokens():
    client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

    # Create wallets and fund them
    issuer_wallet = generate_faucet_wallet(client)
    holder_wallet = generate_faucet_wallet(client)

    # Fetch balances
    issuer_balance = get_balance(issuer_wallet.address, client)
    holder_balance = get_balance(holder_wallet.address, client)

    # Display issuer info
    print(f"Issuer Address: {issuer_wallet.classic_address}")
    print(f"Issuer Balance: {drops_to_xrp(str(issuer_balance))} XRP")

    # Display holder info
    print(f"Holder Address: {holder_wallet.classic_address}")
    print(f"Holder Balance: {drops_to_xrp(str(holder_balance))} XRP")

    # ACCOUNT SET
    account_set_tx = AccountSet(
        account=issuer_wallet.address,
        set_flag=AccountSetAsfFlag.ASF_DEFAULT_RIPPLE
    )

    account_set_result = submit_and_wait(account_set_tx, client, issuer_wallet)

    # Verify the result
    if account_set_result.is_successful():
        print("✅ Account Set tx succeeded: ", account_set_result.result['hash'])
    else:
        print("❌ Account Set tx failed: ", account_set_result.result)

    currency_hex = convert_string_to_hex_padded("BAYES")

    # TRUSTLINE
    trust_set_tx = TrustSet(
        account=holder_wallet.address,
        limit_amount=IssuedCurrencyAmount(
                currency=currency_hex,
                issuer=issuer_wallet.address,
                value="1000",
            )
        )

    trust_set_result = submit_and_wait(trust_set_tx, client, holder_wallet)

    # Verify the result
    if trust_set_result.is_successful():
        print("✅ TrustSet tx succeeded: ", trust_set_result.result['hash'])
    else:
        print("❌ TrustSet tx failed: ", trust_set_result.result)

    # CREATE AMM POOL
    amm_create_tx = AMMCreate(
      account=issuer_wallet.classic_address,
      amount=IssuedCurrencyAmount(
          currency=currency_hex,
          issuer=issuer_wallet.classic_address,
          value="1000",
      ),
      amount2=xrp_to_drops(10),
      trading_fee=100,
   )
    
    amm_create_result = submit_and_wait(amm_create_tx, client, issuer_wallet)
    
    if amm_create_result.is_successful():
      print("✅ AMMCreate transaction succeeded: ", amm_create_result.result['hash'])
    else:
      print("❌ AMMCreate transaction failed: ", amm_create_result.result)

    # SWAP "XRP" FOR "BAYES" (THROUGH THE AMM POOL)
    swap_tx = Payment(
       account=holder_wallet.address,
       destination=holder_wallet.address,
       amount=IssuedCurrencyAmount(
           currency=currency_hex,
           issuer=issuer_wallet.address,
           value="10",
       ),
       send_max=xrp_to_drops(5),
   )

    swap_result = submit_and_wait(swap_tx, client, holder_wallet)

    if swap_result.is_successful():
       print("✅ Swap transaction succeeded: ", swap_result.result['hash'])
    else:
       print("❌ Swap transaction failed: ", swap_result.result)
