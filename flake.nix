{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    py-solc-x-src = {
      url = "github:ApeWorX/py-solc-x/v2.0.5";
      flake = false;
    };
  };

  outputs = {
    nixpkgs,
    flake-utils,
    py-solc-x-src,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};

      inherit (pkgs) mkShell;
      inherit (pkgs.python3Packages) buildPythonPackage;

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

      shell = mkShell {
        name = "blockchain-shell";

        buildInputs =
          [python]
          ++ (with pkgs; [
            solc
            foundry
          ]);
      };
    in {
      devShells.default = shell;
    });
}
