
# How to create and sign offline transaction

[![ICON badge](https://img.shields.io/badge/ICON-blue?logoColor=white&logo=icon&labelColor=31B8BB)](https://shields.io/)

Generate a wallet

```bash
$  ./sign-offline.py genwallet -f keyfile.json -p testtest@#@#
====== Generates a wallet ======
keystore-file : keyfile.json
password : testtest@#@#
wallet address : hx77f8cfea2bbe2cce26a83c9b2b51a112642943cb
wallet private_key : ec239d60904d16aa53ea5f46e5a44703c912cfe7feec32b1cf1bc38b9938b2cc
```

Generate a Transaction without send

```bash
$ ./sign-offline.py gentx -f keyfile.json -p testtest@#@# --to-addr hxa067296997056e507ac2296573472f3c750d8b62 --value 0.1
====== Generate a Transaction ======
signed_data : {'version': '0x3', 'from': 'hx77f8cfea2bbe2cce26a83c9b2b51a112642943cb', 'to': 'hxa067296997056e507ac2296573472f3c750d8b62', 'stepLimit': '0xf4240', 'timestamp': '0x59e4371b91c36', 'nid': '0x50', 'value': '0x16345785d8a0000', 'nonce': '0x64', 'signature': 'xwxTc6n6Yb+tMxROMJB+4iOvaTxxeP0VedcDeoF9vrJ0UZXqfTTNuNZvKJnLwzx13p/hhZ08ek04t0806bSHJgE='}
convert_tx_to_jsonrpc_request : {'version': '0x3', 'from': 'hx77f8cfea2bbe2cce26a83c9b2b51a112642943cb', 'to': 'hxa067296997056e507ac2296573472f3c750d8b62', 'stepLimit': '0xf4240', 'timestamp': '0x59e4371b91d70', 'nid': '0x50', 'value': '0x16345785d8a0000', 'nonce': '0x64'}

```


```bash

$ ./sign-offline.py --help
usage: sign-offline.py [-h] [--url url] [--is-send is_send] [--nid nid]
                       [--value value] [-to to_addr] [-f keystore-file]
                       [-p password]
                       command

Generate Transaction

positional arguments:
  command               gentx, genwallet

optional arguments:
  -h, --help            show this help message and exit
  --url url             Endpoint url
  --is-send is_send     is-send, True/False
  --nid nid             Network ID
  --value value         icx amount
  -to to_addr, --to-addr to_addr
                        to address. default: None
  -f keystore-file, --keystore-file keystore-file
                        keystore filename. default: None
  -p password, --password password
                        keystore's password default: None

```