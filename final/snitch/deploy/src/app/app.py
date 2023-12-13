# Runs an anvil blockchain as well as a Flask application

import subprocess
from eth_account.hdaccount import generate_mnemonic
from eth_account import Account
from flask import Flask, Response, request, abort, render_template
import requests
from web3 import Web3
from time import sleep
from re import findall

Account.enable_unaudited_hdwallet_features()

mnemonic = generate_mnemonic(12, 'english')

deployer_account = Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/0")
deployer_key = deployer_account._private_key.hex()
deployer_address = deployer_account.address

player_account = Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/1")
player_key = player_account._private_key.hex()
player_address = player_account.address

contracts = {}

# this runs in the background
proc = subprocess.Popen(
    args=[
        '/root/.foundry/bin/anvil',
        '--accounts',
        '2',  # first account is the deployer, second account is for the user
        '--balance',
        '1000',
        '--mnemonic',
        mnemonic,
        '--chain-id',
        '1337'
    ],
)

web3 = Web3(Web3.HTTPProvider(f'http://127.0.0.1:8545'))
while True:
    if proc.poll() is not None:
        exit(1)
    if web3.is_connected():
        break
    sleep(0.1)

deployer = subprocess.run([
    '/root/.foundry/bin/forge',
    'create', 
    './src/Setup.sol:Setup', 
    '--value',
    '500ether', 
    '--private-key',
    deployer_key], stdout=subprocess.PIPE, cwd='/blockchain')

result = deployer.stdout.decode()
contracts['Setup'] = findall('Deployed to: (.*)',result)[0]

snitch_proc = subprocess.run([
    '/root/.foundry/bin/cast',
    'storage',
    contracts['Setup'], 
    '0',
    '--rpc-url',
    'http://127.0.0.1:8545'], stdout=subprocess.PIPE, cwd='/blockchain')

contracts['Snitch'] = '0x' + findall('0x00000000000063(.*)3419010100', snitch_proc.stdout.decode())[0]

app = Flask(__name__)

ALLOWED_NAMESPACES = ['web3', 'eth', 'net']

@app.route('/')
def index():
    return render_template('index.html', key=player_key, address=player_address, setup=contracts['Setup'])

# proxies requests to the blockchain after parsing it
@app.route('/rpc', methods=['POST'])
def rpc():
    body = request.get_json()

    allowed = (
        any(body['method'].startswith(namespace)
            for namespace in ALLOWED_NAMESPACES)
        and body['method'] != 'eth_sendUnsignedTransaction'
    )

    if allowed:
        resp = requests.post('http://127.0.0.1:8545', json=body)
        response = Response(resp.content, resp.status_code,
                            resp.raw.headers.items())
        return response

    abort(403)

@app.route('/flag')
def flag():
    contract_balance = subprocess.run([
        '/root/.foundry/bin/cast',
        'balance',
        contracts['Snitch']], stdout=subprocess.PIPE)

    authorities_balance = subprocess.run([
        '/root/.foundry/bin/cast',
        'balance',
        '0xCaffE305b3Cc9A39028393D3F338f2a70966Cb85'], stdout=subprocess.PIPE)

    player_balance = subprocess.run([
        '/root/.foundry/bin/cast',
        'balance',
        player_address], stdout=subprocess.PIPE)

    contract_balance = int(contract_balance.stdout.decode().strip())
    authorities_balance = int(authorities_balance.stdout.decode().strip())
    player_balance = int(player_balance.stdout.decode().strip())

    contract_balance = web3.from_wei(contract_balance, 'ether')
    authorities_balance = web3.from_wei(authorities_balance, 'ether')
    player_balance = web3.from_wei(player_balance, 'ether')

    if contract_balance == 0 and authorities_balance >= 500 and player_balance <= 1000:
        return 'FLAG{71a97c1c1589964559e11fd2d4ef7fd2} => Bl0ckch@in_IS_w0rld_R3ADabl3_AND_ALICE_i$_br0k3'
    else:
        return 'Try again'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
