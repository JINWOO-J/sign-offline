#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from iconsdk.icon_service import IconService
from iconsdk.builder.transaction_builder import CallTransactionBuilder, TransactionBuilder
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet
import argparse


def kvPrint(key,value,color="yellow"):
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
    key_width = 9
    key_value = 3
    print(bcolors.OKGREEN + "{:>{key_width}} : ".format(key, key_width=key_width) + bcolors.ENDC, end="")
    print(bcolors.WARNING + "{:>{key_value}} ".format(str(value), key_value=key_value) + bcolors.ENDC)


def generateTX(file, password, icx_value, to_addr, nid, api_url, is_send):
    step_limit = 1000000
    value = int(icx_value *10 ** 18)
    # kvPrint("value", f"{value:,}")
    wallet = KeyWallet.load(file, password)
    owner_from_addr = wallet.get_address()
    transaction = TransactionBuilder() \
        .from_(owner_from_addr) \
        .to(to_addr) \
        .step_limit(step_limit) \
        .nid(int(nid)) \
        .nonce(100) \
        .value(value) \
        .build()
    signed_data = SignedTransaction(transaction, wallet)
    kvPrint("signed_data", signed_data.signed_transaction_dict)
    kvPrint("convert_tx_to_jsonrpc_request", signed_data.convert_tx_to_jsonrpc_request(transaction, wallet))
    if is_send:
        print("===== send tx =====")
        PROVIDER = HTTPProvider(f"{api_url}/api/v3")
        ICON_SERVICE = IconService(PROVIDER)
        tx_hash = ICON_SERVICE.send_transaction(signed_data)
        kvPrint(f"{file},  sendTX() txResult" , tx_hash)


def generateWallet(file, password):
    from iconsdk.wallet.wallet import KeyWallet
    # Generates a wallet
    wallet = KeyWallet.create()
    # Loads a wallet from a keystore file
    # wallet = KeyWallet.load("./keystore.json", "password")
    # # Stores a keystore file on the file path
    wallet.store(file, password) # throw exception if having an error.
    # Returns an Address
    kvPrint("wallet address", wallet.get_address())
    # Returns a private key
    kvPrint("wallet private_key", wallet.get_private_key())


def get_parser():
    parser = argparse.ArgumentParser(description='Generate Transaction')
    parser.add_argument( 'command', help='gentx, genwallet')
    parser.add_argument('--url', metavar='url', help=f'Endpoint url', default="https://zicon.net.solidwallet.io")
    parser.add_argument('--is-send', metavar='is_send', help=f'is-send, True/False', default=False)
    parser.add_argument('--nid', metavar='nid', type=int, help=f'Network ID', default=80)
    parser.add_argument('--value', metavar='value', type=float, help=f'icx amount', default=0.1)
    parser.add_argument('-to', '--to-addr', metavar='to_addr', default=None, help=f'to address. default: None')
    parser.add_argument('-f', '--keystore-file', metavar='keystore-file', default=None, help=f'keystore filename. default: None')
    parser.add_argument('-p', '--password', metavar='password', default=None, help=f'keystore\'s password default: None')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.command == "gentx":
        print("====== Generate a Transaction ======")
        generateTX(
            file=args.keystore_file,
            password=args.password,
            icx_value=args.value,
            to_addr=args.to_addr,
            nid=args.nid,
            api_url=args.url,
            is_send=args.is_send,
        )
    elif args.command == "genwallet":
        print("====== Generate a wallet ======")
        kvPrint("keystore-file", args.keystore_file)
        kvPrint("password", args.password)
        generateWallet(args.keystore_file, args.password)


if __name__ == '__main__':
    main()
