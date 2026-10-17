#!/usr/bin/env python

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Type

import solcx
from rich import print as rprint
from web3 import Web3
from web3.contract import Contract

from task1_connect import Network
from task3_interraction import Account, Connection, EthUnit
from task4_transaction import TxNew

CUR_DIR: Path = Path(__file__).parent


@dataclass
class SmartContract:
    """
    A smart contract.
    """

    addr: str | None
    """
    A contract address.
    """

    bytecode: bytes | None
    """
    A bytecode.
    """

    abi: list[dict]
    """
    An abi.
    """

    @classmethod
    def compile(cls, file: Path, contract_name: str) -> SmartContract:
        """
        Compiles solidity smart contractd file.
        """

        file_abs = file.absolute()
        file_rel = file_abs.relative_to(Path.cwd())

        compiled = solcx.compile_files(file_abs)

        output_name = f"{file_rel.as_posix()}:{contract_name}"
        output = compiled[output_name]

        return cls(
            addr=None,
            bytecode=Web3.to_bytes(hexstr=output["bin"]),
            abi=output["abi"],
        )

    def deploy(self, con: Connection, acc: Account, ctor_args: list[object]) -> None:
        ctor = self._get_contract(con).constructor(*ctor_args)
        tx_data_str = ctor.data_in_transaction
        tx_data = Web3.to_bytes(hexstr=tx_data_str)

        tx_new = TxNew(acc1, data=tx_data)
        tx_res = tx_new.send(con)

        self.addr = tx_res.contract_addr
        rprint(f"[bold green]Deployed contract: {self.addr}[/bold green]")

    def _get_contract(self, con: Connection) -> Type[Contract]:
        """
        Returns an internal contract representation.
        """

        if self.addr is not None:
            return con.w3.eth.contract(address=self.addr, abi=self.abi)  # type: ignore
        elif self.bytecode is not None:
            return con.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        else:
            rprint("[bold red]A contract hase neither bytecode, nor address[/bold red]")
            exit(1)


if __name__ == "__main__":
    api_key = os.environ["INFURA_API_KEY"]
    acc1_key = os.environ["ACC1_KEY"]

    net = Network.from_name("Sepolia")
    con = Connection.connect(net, api_key)
    acc1 = Account.from_key(con, acc1_key)

    contract = SmartContract.compile(CUR_DIR / "task5_math.sol", "task5_math")
    contract.deploy(con, acc1, [])
