import time
from api import *

TOKEN_ADDR = "0x59bf4fd02a37e31C32b901036A804FCD71d3169f"
TARGETED_WALLETS = [
    "0xa5e1defb98EFe38EBb2D958CEe052410247F4c80"
]

last_transactions = {wallet: None for wallet in TARGETED_WALLETS}

while True:
    for wallet in TARGETED_WALLETS:
        current_transaction = api_get_token_txs(wallet, TOKEN_ADDR)
        if None in current_transaction:
            continue

        current_transaction_tx      = current_transaction[2]

        if current_transaction_tx:
            if not last_transactions[wallet]:
                message             = f"<b>Last transaction for {wallet}:</b>\n" \
                                      f"----------\n" \
                                      f"{current_transaction[0]}\n->\n{current_transaction[1]}\n" \
                                      f"----------\n" \
                                      f"{current_transaction[3]} {current_transaction[4]} {current_transaction[5]}\n" \
                                      f"<a href='{current_transaction[6]}'><b>CHECK ON ETHERSCAN</b></a>"
                # telegram_send_message(message)
                print(message)
                last_transactions[wallet] = current_transaction_tx
            elif last_transactions[wallet] != current_transaction_tx:
                message             = f"<b>New transaction detected for {wallet}:</b>\n" \
                                      f"----------\n" \
                                      f"{current_transaction[0]}\n->\n{current_transaction[1]}\n" \
                                      f"----------\n" \
                                      f"{current_transaction[3]} {current_transaction[4]} {current_transaction[5]}\n" \
                                      f"<a href='{current_transaction[6]}'><b>CHECK ON ETHERSCAN</b></a>"
                # telegram_send_message(message)
                print(message)
                last_transactions[wallet] = current_transaction_tx
        time.sleep(5)
    time.sleep(60)