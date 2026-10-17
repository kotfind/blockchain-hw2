#!/usr/bin/env python

from __future__ import annotations

import os
from dataclasses import dataclass
from sys import exit
from typing import ClassVar, cast

from beaupy import select
from rich import print as rprint
from web3 import HTTPProvider, Web3


@dataclass
class Network:
    """
    A blockchain network.
    """

    LIST: ClassVar[list[Network]] = []
    """
    A list of available networks.
    """

    name: str
    """
    A human-readable name.
    """

    url: str
    """
    A RPC url.

    Does NOT contain an API key.
    """

    def __str__(self):
        return self.name

    @classmethod
    def from_name(cls, name: str) -> Network:
        """
        Returns a network this `LIST` with a given name.
        """

        for net in cls.LIST:
            if net.name == name:
                return net

        rprint(f"[bold red]Failed to find a network called `{name}`[/bold red]")
        exit(1)

    @classmethod
    def pick(cls) -> Network:
        """
        Shows a dialog to pick a network from the `LIST`.
        """

        rprint("[bold]Pick a network to connect to:[/bold]")

        choice = select(cast(list[str | Network], cls.LIST))
        assert isinstance(choice, Network)

        return choice

    def connect(self, api_key: str) -> Web3:
        """
        Connects to the current network.
        """

        url = f"{self.url}/{api_key}"
        w3 = Web3(HTTPProvider(url))

        if w3.is_connected():
            rprint(f"[bold green]Connected to {self.name}[/bold green]")
            return w3

        rprint(f"[bold red]Failed to connect to {self.name}[/bold red]")
        exit(1)


# source: https://docs.infura.io/get-started/endpoints#ethereum
Network.LIST.extend(
    [
        Network("Sepolia", "https://sepolia.infura.io/v3"),
        Network("Hoodi", "https://hoodi.infura.io/v3"),
        Network("Mainnet", "https://mainnet.infura.io/v3"),
        # TODO: ganache
    ]
)

if __name__ == "__main__":
    api_key = os.environ["INFURA_API_KEY"]

    net = Network.pick()

    w3 = net.connect(api_key)
    rprint(f"[bold]Chain ID: {w3.eth.chain_id}[/bold]")
