import requests
import json

API_URL = "https://blockstream.info/api/"
SATS_PER_BTC = 100_000_000
def get_transaction_list(input_address):
    api_end_point = API_URL + f"address/{input_address}/txs"
    response = requests.get(url=api_end_point)
    return response.json()

def calculate_tx_flow(transaction, address):
    vouts = [vout for vout in transaction['vout'] if vout.get('scriptpubkey_address')==address]
    vins = [vin for vin in transaction['vin'] if vin.get('prevout',{}).get('scriptpubkey_address')==address ]
    sum_vout = sum(vout['value'] for vout in vouts)
    sum_vin = sum(vin['prevout']['value'] for vin in vins)
    return sum_vout, sum_vin, sum_vout - sum_vin

def process_address_transactions(address):
    output_transactions = []
    tx_list = get_transaction_list(address)
    for transaction in tx_list:
        txid = transaction['txid']
        receive, spent, net = calculate_tx_flow(transaction,address)
        block_time = transaction['status']['block_time'] if transaction['status']['confirmed']== True else None
        output_transactions.append({
            "txid": txid,
            "address": address,
            "block_time": block_time,
            "received": receive,
            "spent":spent,
            "net":net
        })
    return output_transactions

if __name__ == "__main__":
    input_address = "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s"
    processed_txs = process_address_transactions(input_address)
    print(f"--------Transactions in address: {input_address}")
    for tempTransaction in processed_txs:
        print(f"---Transaction Info for txid: {tempTransaction['txid'][:8]}")
        print(f"Block time: {tempTransaction['block_time']}") 
        print(f"Total received: {tempTransaction['received']/SATS_PER_BTC:.8f}BTC")
        print(f"Total spent: {tempTransaction['spent']/SATS_PER_BTC:.8f}BTC")
        print(f"Net value: {tempTransaction['net']/SATS_PER_BTC:.8f}BTC")
        print("\n")
