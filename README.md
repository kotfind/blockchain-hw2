## Mathematical Methods for Distributed Ledger Systems
## Homework 2. Report
## By Savva Chubiy, БПИ232

### Repo structure

- `flake.nix`, `flake.lock`, `.envrc`

    These files define a nix devShell with direnv support.
    The shell contains all the required dependencies.

    Install `nix` package manager and setup `direnv` tool, than run
    `direnv allow` from the repo root to enable the devShell.

- `VALUES.md`

    Provides all the values (tx ids, account addresses, etc.) required in the
    assignment. And some extra info.

- `src/*`

    Each `task{i}` file (or group of files) is a solution to task `i`.

    All the python files are both executables and libraries.
    That is, each file can be either run individually or be included from another file.

### Remarks

- If you want the scripts to actually work, you should define all the env vars,
  listed in `VALUES.md`.

  Alternatively, you can write those in `.env` file and rerun `direnv allow`.

- I didn't use Remix IDE. Instead, I used NVim + Solidity LSP to write code
    and custom script (`./src/task5_contract_deploy.py`) to deploy it.

- I used Anvil instead of Ganache as later is deprecated.
