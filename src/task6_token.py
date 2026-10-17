#!/usr/bin/env python

import os
from pathlib import Path
from sys import exit

from beaupy import confirm
from rich import print as rprint

from task1_connect import Network
from task3_interraction import Account, Connection
from task5_contract_deploy import SmartContract

ROOT: Path = Path(__file__).parents[1]

if __name__ == "__main__":
    api_key = os.environ["INFURA_API_KEY"]
    acc2_key = os.environ["ACC2_KEY"]
    dst_acc_addr = os.environ["TASK6_DST_ACC_ADDR"]

    net = Network.from_name("Sepolia")
    con = Connection.connect(net, api_key)
    acc2 = Account.from_key(con, acc2_key)

    contract = SmartContract.compile(ROOT / "src" / "task6_token.sol", "task6_token")

    if not confirm(f"Do you want to deploy new NYA token contract?"):
        rprint("[bold red]Confirmation failed[/bold red]")
        exit(1)

    contract.deploy(con, acc2, [])

    base_in_nya = contract.get(con, "baseInNya")
    assert isinstance(base_in_nya, int)

    amount_nya = 10
    amount_base = amount_nya * base_in_nya

    if not confirm(
        f"Do you want to send {amount_nya} NYA from {acc2.addr} to {dst_acc_addr}?"
    ):
        rprint("[bold red]Confirmation failed[/bold red]")
        exit(1)

    contract.call(con, acc2, "transfer", [dst_acc_addr, amount_base])
