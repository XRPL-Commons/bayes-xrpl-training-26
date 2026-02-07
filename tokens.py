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
    client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

    # Create and fund wallets
    issuer_wallet = generate_faucet_wallet(client)
    holder_wallet = generate_faucet_wallet(client)

    # Get balances
    issuer_balance = get_balance(issuer_wallet.address, client)
    holder_balance = get_balance(holder_wallet.address, client)

    # Display wallet info
    print(f"Issuer: {issuer_wallet.address}")
    print(f"Issuer balance: {drops_to_xrp(str(issuer_balance))} XRP")

    print(f"Holder: {holder_wallet.address}")
    print(f"Holder balance: {drops_to_xrp(str(holder_balance))} XRP")

    # Enable Default Ripple on issuer account
    account_set_tx = AccountSet(
        account=issuer_wallet.address,
        set_flag=AccountSetAsfFlag.ASF_DEFAULT_RIPPLE,
    )

    account_set_result = submit_and_wait(account_set_tx, client, issuer_wallet)

    if account_set_result.is_successful():
        print(f"AccountSet transaction validated successfully: {account_set_result.result['hash']}")
    else:
        print("AccountSet transaction failed to validate: ", account_set_result.result)

    # Create TrustLine from holder to issuer
    currency_hex = convert_string_to_hex_padded("MYTOKEN")

    trust_set_tx = TrustSet(
        account=holder_wallet.address,
        limit_amount=IssuedCurrencyAmount(
            currency=currency_hex,
            issuer=issuer_wallet.address,
            value="1000",
        ),
    )

    trust_set_result = submit_and_wait(trust_set_tx, client, holder_wallet)

    if trust_set_result.is_successful():
        print(f"TrustSet transaction validated successfully: {trust_set_result.result['hash']}")
    else:
        print("TrustSet transaction failed to validate: ", trust_set_result.result)
        
    # Create AMM Pool
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
       print(f"AMMCreate transaction validated successfully: {amm_create_result.result['hash']}")
    else:
       print("AMMCreate transaction failed to validate: ", amm_create_result.result)
