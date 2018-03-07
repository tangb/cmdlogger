# cmdlogger
Runs specified command, watchs for stdout/stderr and sends output to socket server.

This python program was originally created to monitor Windows command launched under UAC elevated privileges using ShellExecuteEx.

Windows ShellExecuteEx function prevents stdout/stderr from being displayed in console (in fact there is no console).
This program is only a workaround for that problem.

# Installation
This program runs with Python2.7.X and Python3.X and requires no extra library.

# How to use
## Windows
Launch Windows command using ShellExecuteEx (no console window and UAC elevation):
```
command = [u'mycommand.sh', u'param1']
user_cmd = command[0]
user_cmd_params = [u'param1', u'param2'] + command[1:]
proc_info = ShellExecuteEx(nShow=win32con.SW_HIDE, fMask=shellcon.SEE_MASK_NOCLOSEPROCESS, lpVerb=u'runas', lpFile=cmd, lpParameters=params)
```

And inspires next part of your code with test/server.py sample.

## Mac
This is an example of how to run command with admin privileges using cmdlogger on Mac environment:
```
command = [u'mycommand.sh', u'param1']
params = [cmdlogger_path, comm_port, self.command[0]] + self.command[1:]
cmd_line = 'osascript -e "do shell script \\"%s\\" with administrator privileges"' % u' '.join(params)
proc_info = subprocess.Popen(cmd_line, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=self.on_posix)
```

## Linux
This is an example of how to run command with admin privileges using cmdlogger on Linux environment:
```
command = [u'mycommand.sh', u'param1']
params = [cmdlogger_path, comm_port, self.command[0]] + self.command[1:]
cmd_line = 'pkexec %s' % u' '.join(params)
proc_info = subprocess.Popen(cmd_line, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=self.on_posix)
```

## Full example
You can find full usage example in [console.py](https://github.com/tangb/CleepDesktop/blob/master/core/libs/console.py) on CleepDesktop project 

# Build
Install build dependency [Pyinstaller](http://www.pyinstaller.org/) running in console:
> pip3 install -r requirements

Now build a standalone executable running:
> build.bat or build.sh

Then run 7zip to compress archive:
> 7z.exe a cmdlogger-[target].7z dist\cmdlogger\

## Releases
You can find precompiled version for different environment into dist/ folder.

# Troubleshoot
If you get this error:
```
IndexError: tuple index out of range
pip install https://github.com/pyinstaller/pyinstaller/archive/develop.zip
```
Please install pyinstaller devel version that supports python 3.6 (latest official release 3.3.1 officialy support python 3.6)

# Tests
You can launch tests using test/server.py script:
> python3 server.py

And launch cmdlogger with parameters:
> python3 cmdlogger.py 9001 test\test.bat

9001 is the hardcoded port in server.py
