{pkgs}: {
  deps = [
    pkgs.python312Packages.flask-wtf
    pkgs.postgresql_12
  ];
}
