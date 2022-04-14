#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from iconsdk.icon_service import IconService
from iconsdk.builder.transaction_builder import CallTransactionBuilder, TransactionBuilder
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet
import argparse
import json
import time

from iconsdk.libs.serializer import generate_message, serialize


def current_milli_time():
    return round(time.time() * 1000)


def kvPrint(key, value, color="yellow"):
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


def generate_tx(file, password, icx_value, to_addr, nid, api_url, is_send, timestamp):
    step_limit = 1000000
    value = int(icx_value * 10 ** 18)
    wallet = KeyWallet.load(file, password)
    owner_from_addr = wallet.get_address()
    transaction = TransactionBuilder() \
        .from_(owner_from_addr) \
        .to(to_addr) \
        .step_limit(step_limit) \
        .nid(int(nid)) \
        .nonce(100) \
        .value(value) \
        .timestamp(timestamp)\
        .build()
    signed_params = SignedTransaction(transaction, wallet)
    signed_payload = {'jsonrpc': '2.0', 'method': "icx_sendTransaction", 'id': 1234, "params": signed_params.signed_transaction_dict}
    kvPrint("[before] signed_payload", json.dumps(signed_payload, indent=4, sort_keys=True))
    kvPrint("[before] calculate the tx_hash", f"0x{generate_message(signed_params.signed_transaction_dict)}")

    if is_send:
        print("===== send tx =====")
        provider = HTTPProvider(f"{api_url}/api/v3")
        icon_service = IconService(provider)
        tx_hash = icon_service.send_transaction(signed_params)
        kvPrint(f"[after]  sendTX() txResult", tx_hash)

    return signed_payload


def generate_wallet(file, password):
    from iconsdk.wallet.wallet import KeyWallet
    # Generates a wallet
    wallet = KeyWallet.create()
    # Loads a wallet from a keystore file
    # wallet = KeyWallet.load("./keystore.json", "password")
    # # Stores a keystore file on the file path
    wallet.store(file, password)  # throw exception if having an error.
    # Returns an Address
    kvPrint("wallet address", wallet.get_address())
    # Returns a private key
    kvPrint("wallet private_key", wallet.get_private_key())


def get_parser():
    parser = argparse.ArgumentParser(description='Generate Transaction')
    parser.add_argument('command', help='gentx, genwallet')
    parser.add_argument('--url', metavar='url', help=f'Endpoint url', default="https://sejong.net.solidwallet.io")
    parser.add_argument('--is-send', metavar='is_send', help=f'is-send, True/False', default=False)
    parser.add_argument('--nid', metavar='nid', type=int, help=f'Network ID MainNet: 1, TestNet: 2, sejong: 83 ', default=83)
    parser.add_argument('--value', metavar='value', type=float, help=f'icx amount', default=0.1)
    parser.add_argument('-to', '--to-addr', metavar='to_addr', default=None, help=f'to address. default: None')
    parser.add_argument('-f', '--keystore-file', metavar='keystore-file', default=None, help=f'keystore filename. default: None')
    parser.add_argument('-p', '--password', metavar='password', default=None, help=f'keystore\'s password default: None')
    parser.add_argument('-a', '--after-min', metavar='after-min', default=None, help=f'after minutes')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.command == "gentx":
        print("====== Generate a Transaction ======")
        after_min = None
        if args.after_min:
            after_min = current_milli_time() + int(args.after_min) * 1000 * 60
            print(f"Now: {current_milli_time()}, After {args.after_min} min : {after_min}")

        generate_tx(
            file=args.keystore_file,
            password=args.password,
            icx_value=args.value,
            to_addr=args.to_addr,
            nid=args.nid,
            api_url=args.url,
            is_send=args.is_send,
            timestamp=after_min
        )
    elif args.command == "genwallet":
        print("====== Generate a wallet ======")
        kvPrint("keystore-file", args.keystore_file)
        kvPrint("password", args.password)
        generate_wallet(args.keystore_file, args.password)


if __name__ == '__main__':
    main()
