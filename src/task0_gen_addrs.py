#!/usr/bin/env python

from shlex import quote

from web3 import Web3

w3 = Web3()

print("Add these to .env:\n")
for i in range(1, 3):
    acc = w3.eth.account.create()

    print(f"ACC{i}_ADDR={quote(acc.address)}")
    print(f"ACC{i}_KEY={quote(w3.to_hex(acc.key))}")
