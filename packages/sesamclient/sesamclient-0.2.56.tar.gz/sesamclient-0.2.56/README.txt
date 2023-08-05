To build a static executable file for the sesamclient, use the "build_with_pyinstaller" Makefile target, like this:

  # make a python3.5 virtualenv, since the Makefile uses "pip install"
  cd lake/python/client
  virtualenv -p python3.5 .venv
  . .venv/bin/activate

  make build_with_pyinstaller

  # test that the resulting executable works:
  ./dist/sesam --help
