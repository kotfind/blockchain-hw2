#!/usr/bin/env python

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import ClassVar

from rich import print as rprint
from web3 import Web3
from web3.types import BlockData

from task1_connect import Network


@dataclass
class Connection:
    """
    A wrapper over Web3, that provide some usefull methods.
    """

    w3: Web3
    """
    An inner Web3 object.
    """

    @classmethod
    def connect(cls, net: Network, api_key: str) -> Connection:
        """
        Connects to a given network.
        """

        w3 = net.connect(api_key)
        return cls(w3)

    def get_block_number(self) -> int:
        """
        Return the last block's number.
        """

        return self.w3.eth.get_block_number()

    def get_block_info(self, number: int | None = None) -> BlockInfo:
        """
        Return some info about a block with a given number.

        If no number is provided, return info about the last block.
        """

        ident = "latest" if number is None else number
        block = self.w3.eth.get_block(ident)
        return BlockInfo.from_block(block)

@dataclass
class BlockInfo:
    """
    Some common info about a block.
    """

    number: int
    """
    A block number.
    """

    hash: str
    """
    A block hash.
    """

    time: datetime
    """
    A block datetime.
    """

    @classmethod
    def from_block(cls, block: BlockData) -> BlockInfo:
        return cls(
            number=block.number, # ty: ignore
            hash=block.hash.hex(), # ty: ignore
            time=datetime.fromtimestamp(block.timestamp, tz=timezone.utc) # ty: ignore
        )

@dataclass
class EthUnit:
    """
    An Etherium money unit.
    """

    wei: int
    """
    An internal ammount, in Wei.
    """

    WEI_IN_ETH: ClassVar[int] = 10**18
    """
    An amount of Wei in a single Eth.
    """

    @classmethod
    def from_wei(cls, wei: int) -> EthUnit:
        return cls(wei)

    def to_wei(self) -> int:
        """
        Covnerts to Wei.
        """

        return self.wei

    def to_eth_float(self) -> float:
        """
        Converts to Eth.

        **Beware of `float` numbers precision.**
        """

        return self.wei / EthUnit.WEI_IN_ETH


@dataclass
class Account:
    """
    An Etherium account.
    """

    addr: str
    """
    An account address.
    """

    key: str
    """
    An account key.
    """

    def get_balance(self, con: Connection) -> EthUnit:
        wei = con.w3.eth.get_balance(self.addr) # ty: ignore
        return EthUnit.from_wei(wei)

if __name__ == "__main__":
    api_key = os.environ["INFURA_API_KEY"]
    acc1_addr = os.environ["ACC1_ADDR"]
    acc1_key = os.environ["ACC1_KEY"]

    net = Network.from_name("Sepolia")
    con = Connection.connect(net, api_key)
    acc1 = Account(acc1_addr, acc1_key)

    rprint(f"[bold]Block height: {con.get_block_number()}[/bold]")

    info = con.get_block_info()
    rprint(
        "[bold]"
        "Block info:\n"
        f"  Number: {info.number}\n"
        f"  Hash: {info.hash}\n"
        f"  Time: {info.time.astimezone().isoformat()}"
        "[/bold]")

    balance = acc1.get_balance(con)
    rprint(f"[bold]Balance on {acc1.addr}:\n  {balance.to_wei()} WEI = {balance.to_eth_float():.5g} ETH[/bold]")

