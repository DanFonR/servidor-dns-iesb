let
  pkgs = import <nixpkgs> {};
in
  pkgs.mkShell {
    packages = with pkgs; [
      # (pkgs.python313.withPackages (ps:
      #   with ps; [
      #     flask
      #     flask-cors
      #     flask-jwt-extended
      #   ]))
      nodePackages_latest.nodejs
      typescript-language-server
    ];
  }
