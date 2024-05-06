"""
主动进行链上转账
"""
from web3 import Web3, HTTPProvider
import json

web3 = Web3(HTTPProvider("https://devnet.zama.ai"))

print(web3.is_connected())

# Initialize the address calling the functions/signing transactions
caller = "0x21b7356966eAef9C6CCBeB81a226630A9c916797"
private_key = "b009e7bbd3b2103dc8f7f3ba14a6704fa929eaa9a490c005c479bae902c131bb"

# Initialize address nonce
nonce = web3.eth.get_transaction_count(caller)

# Initialize contract ABI and address
with open('contracts/EncryptedERC20.abi', 'r') as f:
    abi = json.load(f)

contract_address = "0x390DCAAc12e5Bf1bd9c44EeA3707728A2F851125"

# Create smart contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)

# initialize the chain id, we need it to build the transaction for replay protection
Chain_id = web3.eth.chain_id

# Call your function
call_function = contract.functions.cross_chain_transfer(Web3.to_bytes(1)).build_transaction({"chainId": Chain_id, "from": caller, "nonce": nonce})

# Sign transaction
signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)

# Send transaction
send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

# Wait for transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)
print(tx_receipt) # Optional

# # call
# totalSupply = contract.functions.totalSupply().call()  # read the coin total supply - call means we are reading from the blockchain
# print("totalSupply:" + str(totalSupply))
