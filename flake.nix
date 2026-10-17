{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    py-solc-x-src = {
      url = "github:ApeWorX/py-solc-x/v2.0.5";
      flake = false;
    };
    solidity-language-server-src = {
      url = "github:asyncswap/solidity-language-server";
      flake = false;
    };
  };

  outputs = {
    nixpkgs,
    flake-utils,
    py-solc-x-src,
    solidity-language-server-src,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};

      inherit (pkgs) mkShell;
      inherit (pkgs.python3Packages) buildPythonPackage;
      inherit (pkgs.rustPlatform) buildRustPackage;

      py-solc-x = buildPythonPackage {
        pname = "py-solc-x";
        version = "2.0.5";
        pyproject = true;

        src = py-solc-x-src;

        build-system = with pkgs.python3Packages; [
          setuptools
          setuptools-scm
          wheel
        ];

        dependencies = with pkgs.python3Packages; [
          requests
          packaging
        ];
      };

      python = pkgs.python3.withPackages (
        pypkgs:
          [py-solc-x]
          ++ (with pypkgs; [
            web3
            beaupy
          ])
      );

      solidity-language-server = buildRustPackage {
        pname = "solidity-language-server";
        version = "0.1.35";
        src = solidity-language-server-src;
        cargoHash = "sha256-4m7ei/DCMwE2E9JjhXi9ibXn24OhMI7UMvwe3xNnhUA=";
        doCheck = false;
      };

      shell = mkShell {
        name = "blockchain-shell";

        buildInputs =
          [python]
          ++ (with pkgs; [
            solidity-language-server
            foundry
            solc
          ]);
      };
    in {
      devShells.default = shell;
    });
}
