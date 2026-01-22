import requests

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

if __name__ == "__main__":
    input_address = "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s"
    tx_list = get_transaction_list(input_address)
    print(f"--------Transactions in address: {input_address}")
    for tempTransaction in tx_list:
        receive, spent, net = calculate_tx_flow(transaction=tempTransaction, address=input_address)
        print(f"---Transaction Info for txid: {tempTransaction['txid'][:8]}") 
        print(f"Total received: {receive/SATS_PER_BTC:.8f}BTC")
        print(f"Total spent: {spent/SATS_PER_BTC:.8f}BTC")
        print(f"Net value: {net/SATS_PER_BTC:.8f}BTC")
        print("\n")