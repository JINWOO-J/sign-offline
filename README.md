
# How to create and sign offline transaction

[![ICON badge](https://img.shields.io/badge/ICON-blue?logoColor=white&logo=icon&labelColor=31B8BB)](https://shields.io/)

Generate a wallet

```bash
$  ./sign-offline.py genwallet -f keyfile.json -p testtest@#@#
====== Generate a wallet ======
keystore-file : keyfile.json
 password : testtest@#@#
wallet address : hxb793e43ede4f2cbc7b9475ca4a443f48e54aba90
wallet private_key : 5f4277163e0624531cf7f2a363fbb65c82c90bfb6bd5f03a85ee1c7206339bed
```

Generate a Transaction without send

```bash
$ ./sign-offline.py gentx -f keyfile.json -p testtest@#@# --to-addr hxa067296997056e507ac2296573472f3c750d8b62 --value 0.1
====== Generate a Transaction ======
signed_payload : {
    "id": 1234,
    "jsonrpc": "2.0",
    "method": "icx_sendTransaction",
    "params": {
        "from": "hxb793e43ede4f2cbc7b9475ca4a443f48e54aba90",
        "nid": "0x50",
        "nonce": "0x64",
        "signature": "J8y3lk8Hbnn8YRvjGDPbhwQZiYWvPhDlQn5UdXSIKigEsSOjh/SctC/BOsff/WiDTevmrMxQfv0iABS8HrpJygA=",
        "stepLimit": "0xf4240",
        "timestamp": "0x59fda251768ce",
        "to": "hxa067296997056e507ac2296573472f3c750d8b62",
        "value": "0x16345785d8a0000",
        "version": "0x3"
    }
}
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
  --nid nid             Network ID MainNet: 1, TestNet: 2, zicon: 80
  --value value         icx amount
  -to to_addr, --to-addr to_addr
                        to address. default: None
  -f keystore-file, --keystore-file keystore-file
                        keystore filename. default: None
  -p password, --password password
                        keystore's password default: None
```