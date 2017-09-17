@echo off
rmdir /Q /S __pycache__
rmdir /Q /S dist\cmdlogger
rmdir /Q /S build
pyinstaller --clean --noconfirm --windowed --noupx --debug --log-level INFO cmdlogger.spec
rmdir /Q /S __pycache__
rmdir /Q /S build