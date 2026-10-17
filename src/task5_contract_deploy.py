#!/usr/bin/env python

import os
from dataclasses import dataclass
from pathlib import Path
from sys import exit

import solcx
from rich import print as rprint
from web3 import Web3
from web3.contract import Contract

from task1_connect import Network
from task3_interraction import Account, Connection
from task4_transaction import TxNew

ROOT: Path = Path(__file__).parents[1]


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
    def compile(
        cls, file: Path, contract_name: str, addr: str | None = None
    ) -> SmartContract:
        """
        Compiles solidity smart contractd file.
        """

        file_abs = file.absolute()
        file_rel = file_abs.relative_to(Path.cwd())

        compiled = solcx.compile_files(file_abs)

        output_name = f"{file_rel.as_posix()}:{contract_name}"
        output = compiled[output_name]

        return cls(
            addr=addr,
            bytecode=Web3.to_bytes(hexstr=output["bin"]),
            abi=output["abi"],
        )

    def deploy(self, con: Connection, acc: Account, ctor_args: list[object]) -> None:
        """
        Deploes a contract.
        """

        ctor = self._get_contract(con).constructor(*ctor_args)
        tx_data_str = ctor.data_in_transaction
        tx_data = Web3.to_bytes(hexstr=tx_data_str)

        tx_new = TxNew(acc, data=tx_data)
        tx_res = tx_new.send(con)

        self.addr = tx_res.contract_addr
        rprint(f"[bold green]Deployed contract: {self.addr}[/bold green]")

    def call(
        self, con: Connection, acc: Account, func_name: str, args: list[object]
    ) -> None:
        """
        Calls a contract's function.
        """

        contract = self._get_contract(con)

        tx_data = Web3.to_bytes(hexstr=contract.encode_abi(func_name, args))

        tx_new = TxNew(acc, self.addr, data=tx_data)
        tx_new.send(con)

    def get(self, con: Connection, value_name: str) -> object:
        """
        Get's a value from state.
        """

        contract = self._get_contract(con)
        value = contract.functions[value_name].call()

        return value

    def _get_contract(self, con: Connection) -> type[Contract]:
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

    contract = SmartContract.compile(ROOT / "src" / "task5_math.sol", "task5_math")
    contract.deploy(con, acc1, [])

    rprint(f"[bold]orig value = {contract.get(con, "res")}[/bold]")

    contract.call(con, acc1, "add", [1, 2])
    rprint(f"[bold]1 + 2 = {contract.get(con, "res")}[/bold]")

    contract.call(con, acc1, "sub", [1, 2])
    rprint(f"[bold]1 - 2 = {contract.get(con, "res")}[/bold]")

    contract.call(con, acc1, "mul", [1, 2])
    rprint(f"[bold]1 * 2 = {contract.get(con, "res")}[/bold]")

    contract.call(con, acc1, "div", [1, 2])
    rprint(f"[bold]1 / 2 = {contract.get(con, "res")}[/bold]")
