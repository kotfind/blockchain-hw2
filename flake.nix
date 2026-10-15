{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};

      inherit (pkgs) mkShell;

      python = pkgs.python3.withPackages (pypkgs:
        with pypkgs; [
          web3
          beaupy
        ]);

      shell = mkShell {
        name = "blockchain-shell";

        buildInputs = [python];
      };
    in {
      devShells.default = shell;
    });
}
