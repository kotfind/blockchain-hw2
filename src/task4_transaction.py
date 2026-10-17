#!/usr/bin/env python

from __future__ import annotations

import os
from dataclasses import dataclass
from sys import exit

from beaupy import confirm
from rich import print as rprint
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

    to_addr: str
    """
    A receiver address.
    """

    amount: EthUnit
    """
    An amount of Eth to send.
    """

    gasLimit: int | None = None
    """
    A maximum amount of gas to spend on a transaction.
    """

    def send(self, con: Connection) -> TxRes:
        """
        Sends the current transaction.
        """

        nonce = con.w3.eth.get_transaction_count(self.from_acc.addr)  # pyright: ignore

        base_fee = con.w3.eth.get_block("pending").baseFeePerGas  # pyright: ignore
        priority_fee = con.w3.eth.max_priority_fee
        max_fee = int(base_fee * 1.5 + priority_fee)

        if self.gasLimit is None:
            gas = con.w3.eth.estimate_gas(
                TxParams(
                    {
                        "from": self.from_acc.addr,
                        "to": self.to_addr,
                        "value": self.amount.to_wei(),  # pyright: ignore
                    }
                )
            )

            rprint(f"[bold]Estimated gas: {gas}[/bold]")
        else:
            gas = self.gasLimit

        tx_data = {
            "from": self.from_acc.addr,
            "to": self.to_addr,
            "value": self.amount.to_wei(),
            "gas": gas,
            "nonce": nonce,
            "maxFeePerGas": max_fee,
            "maxPriorityFeePerGas": priority_fee,
            "chainId": con.w3.eth.chain_id,
        }

        tx_signed = con.w3.eth.account.sign_transaction(tx_data, self.from_acc.key)
        tx_hash_bytes = con.w3.eth.send_raw_transaction(tx_signed.raw_transaction)
        tx_hash = f"0x{tx_hash_bytes.hex()}"
        rprint(f"[bold]Formed transaction {tx_hash}[/bold]")

        receipt = con.w3.eth.wait_for_transaction_receipt(tx_hash_bytes)

        if receipt["status"] == 0:
            rprint(f"[bold red]Transaction {tx_hash} failed[/bold red]")
            exit(1)

        rprint(f"[bold green]Transaction {tx_hash} succeeded[/bold green]")

        return TxRes(self, tx_hash, receipt["blockNumber"])


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
