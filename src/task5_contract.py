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

    bytecode: bytes
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
            bytecode=Web3.to_bytes(hexstr=output["bin"]),
            abi=output["abi"],
        )

    def to_deploy_tx_data(self, con: Connection, ctor_args: list[object]) -> bytes:
        """
        Returns bytes to be sent in transaction's `data` field to deploy contract.
        """

        ctor = self._get_contract(con).constructor(*ctor_args)
        data_str = ctor.data_in_transaction

        return Web3.to_bytes(hexstr=data_str)

    def _get_contract(self, con: Connection) -> Type[Contract]:
        """
        Returns an internal contract representation.
        """

        return con.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)


if __name__ == "__main__":
    api_key = os.environ["INFURA_API_KEY"]
    acc1_key = os.environ["ACC1_KEY"]

    net = Network.from_name("Sepolia")
    con = Connection.connect(net, api_key)
    acc1 = Account.from_key(con, acc1_key)

    contract = SmartContract.compile(CUR_DIR / "task5_math.sol", "task5_math")
    contract_tx_data = contract.to_deploy_tx_data(con, [])

    tx_new = TxNew(acc1, data=contract_tx_data)
    tx_res = tx_new.send(con)

    rprint(f"[bold green]Deployed contract: {tx_res.contract_addr}[/bold green]")
