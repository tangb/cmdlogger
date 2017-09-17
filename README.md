# cmdlogger
Runs specified command, watchs for stdout/stderr and sends output to socket server.

This program was originally created to monitor Windows command launched under UAC elevated privileges using ShellExecuteEx.

Windows ShellExecuteEx function prevents stdout/stderr from being displayed in console (in fact there is no console)
This program is only a workaround for that problem.

# Installation
This program runs with Python2.7.X and Python3.X and requires no extra library.

# Build
Install build dependency [Pyinstaller](http://www.pyinstaller.org/) running in windows console:
```
pip3 install -r requirements
```
Now build a standalone executable running:
```
./build.bat
```

# Tests
You can launch tests using test/server.py script:
```
python3 server.py
```
And launch cmdlogger with parameters:
```
python3 cmdlogger.py 9001 test\test.bat
```
9001 is the hardcoded port in server.py
