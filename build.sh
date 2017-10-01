#!/bin/bash
/bin/rm -rf __pycache__
/bin/rm -rf dist\cmdlogger
/bin/rm -rf build
/usr/local/bin/pyinstaller --clean --noconfirm --windowed --noupx --debug --log-level INFO cmdlogger.spec
/bin/rm -rf __pycache__
/bin/rm -rf build
