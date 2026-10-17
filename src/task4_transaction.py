#!/usr/bin/env python

from __future__ import annotations

import os
from dataclasses import dataclass, field
from sys import exit

from beaupy import confirm
from rich import print as rprint
from web3 import Web3
from web3.types import TxParams

from task1_connect import Network
from task3_interraction import Account, Connection, EthUnit


@dataclass
class TxNew:
    """
    A data, required to send a transaction.
    """

    from_acc: Account
    """
    A sender account.
    """

    to_addr: str | None = None
    """
    A receiver address.
    """

    amount: EthUnit = field(default_factory=lambda: EthUnit.from_wei(0))
    """
    An amount of Eth to send.
    """

    gasLimit: int | None = None
    """
    A maximum amount of gas to spend on a transaction.
    """

    data: bytes | None = None
    """
    A transaction data.
    """

    def send(self, con: Connection) -> TxRes:
        """
        Sends the current transaction.
        """

        nonce = con.w3.eth.get_transaction_count(self.from_acc.addr)  # pyright: ignore

        base_fee = con.w3.eth.get_block("pending").baseFeePerGas  # pyright: ignore
        priority_fee = con.w3.eth.max_priority_fee
        max_fee = int(base_fee * 1.5 + priority_fee)

        tx_data = {
            "from": self.from_acc.addr,
            "value": self.amount.to_wei(),
            "nonce": nonce,
            "maxFeePerGas": max_fee,
            "maxPriorityFeePerGas": priority_fee,
            "chainId": con.w3.eth.chain_id,
        }

        if self.to_addr is not None:
            tx_data["to"] = self.to_addr

        if self.data is not None:
            tx_data["data"] = Web3.to_hex(self.data)

        if self.gasLimit is not None:
            tx_data["gas"] = self.gasLimit
        else:
            tx_data["gas"] = con.w3.eth.estimate_gas(TxParams(**tx_data))
            rprint(f"[bold]Estimated gas: {tx_data['gas']}[/bold]")

        tx_signed = con.w3.eth.account.sign_transaction(tx_data, self.from_acc.key)
        tx_hash_bytes = con.w3.eth.send_raw_transaction(tx_signed.raw_transaction)
        tx_hash = Web3.to_hex(tx_hash_bytes)
        rprint(f"[bold]Formed transaction {tx_hash}[/bold]")

        receipt = con.w3.eth.wait_for_transaction_receipt(tx_hash_bytes)

        if receipt["status"] == 0:
            rprint(f"[bold red]Transaction {tx_hash} failed[/bold red]")
            exit(1)

        rprint(f"[bold green]Transaction {tx_hash} succeeded[/bold green]")

        return TxRes(self, tx_hash, receipt["blockNumber"], receipt["contractAddress"])


@dataclass
class TxRes:
    """
    A result of sending transaction.
    """

    new: TxNew
    """
    An original transaction data.
    """

    hash: str
    """
    A transaction hash.
    """

    block_number: int
    """
    A number of block with the current transaction.
    """

    contract_addr: str | None
    """
    An address of a deployed contract.
    """


if __name__ == "__main__":
    api_key = os.environ["INFURA_API_KEY"]
    acc1_key = os.environ["ACC1_KEY"]
    acc2_addr = os.environ["ACC2_ADDR"]

    net = Network.from_name("Sepolia")
    con = Connection.connect(net, api_key)
    acc1 = Account.from_key(con, acc1_key)

    amount = EthUnit.pick()
    tx_new = TxNew(acc1, acc2_addr, amount)

    if not confirm(
        f"[bold]Do you want to send {amount.to_wei()} WEI from {acc1.addr} to {acc2_addr}[/bold]"
    ):
        rprint("[bold red]Confirmation failed[/bold red]")
        exit(1)

    tx_res = tx_new.send(con)

    rprint(
        "[bold]"
        "Transaction info:\n"
        f"  Hash:     {tx_res.hash}\n"
        f"  Block No: {tx_res.block_number}"
        "[/bold]"
    )
