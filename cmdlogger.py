#! python3

"""
CmdLogger executes specified command in subprocess, watch for command stdout/stderr and return it via socket

Usage: cmdlogger.exe <comm port> <command> <command arg1> <command arg2> ...
 - <comm port>: communication port to send stdout and stderr message to (uses socket)
 - <command>: command to execute
 - <command arg>: command arguments
"""

import signal
import subprocess
import time
import sys
import socket
import logging
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
from threading import Thread
import platform

#init logger
logging.basicConfig(level=logging.WARN, format='%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')
logger = logging.getLogger('CmdLogger')
logger.setLevel(logging.DEBUG)

#constants
VERSION = '0.2.3'

#globals
stdout_queue = Queue()
stderr_queue = Queue()
running = True
client = None
return_code = 1 #general error code returned by default

def enqueue_output(output, queue):
    """
    Enqueue output
    
    Args:
        output (filedescriptor) : output to look
        queue (Queue): Queue instance
    """
    global running
    
    for line in iter(output.readline, b''):
        if not running:
            break
        queue.put(line.strip())
    try:
        output.close()
    except:
        pass
        
def usage():
    """
    Display usage
    """
    print('Usage: cmdlogger(.exe) <comm port> <command> <command args, ...>')
    print(' - comm port: communication port to send stdout and stderr message to (uses socket)')
    print(' - command: command to execute')
    print(' - command args: command arguments')
    print('')
    print('Exit codes:')
    print(' - 0: success')
    print(' - 1: general error (typically invalid parameter)')
    print(' - x: specified command exit code')
    print('')
    print('Cmdlogger version %s' % VERSION)
    
def send_output(output, stdout):
    """
    Send output to server
    
    Args:
        output (string): output to send
        stdout (bool): True if stdout, False for stderr
    """
    global logger, client
    
    if output is None or len(output)==0:
        return
    
    try:
        if stdout:
            logger.debug(u'Send stdout')
            client.send(b'STDOUT:'+output)
        else:
            logger.debug(u'Send stderr')
            client.send(b'STDERR:'+output)
    except:
        logger.exception('Problem sending output. Disable data sending: ')
        client = None

#parse command line arguments
args = sys.argv[1:]
logger.debug(u'Args: %s' % args)
if len(args)<=1:
    usage()
    sys.exit(1)
try:
    comm_port = int(args[0])
    logger.debug(u'Port: %d' % comm_port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((u'127.0.0.1', comm_port))
except:
    logger.exception(u'Unable to init communication socket. Data sending disabled.')
    client = None
command = '"%s"' % args[1]
if len(args)>=2:
    command_args = u' '.join([u'"%s"' % (x,) for x in args[2:]])
logger.debug(u'command:%s command_args:%s' % (command, command_args))

#launch command
logger.debug(u'Launch command')
p = subprocess.Popen(u'%s %s' % (command, command_args), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
pid = p.pid

#async stdout reading
stdout_thread = Thread(target=enqueue_output, args=(p.stdout, stdout_queue))
stdout_thread.daemon = True
stdout_thread.start()

#async stderr reading
stderr_thread = Thread(target=enqueue_output, args=(p.stderr, stdout_queue))
stderr_thread.daemon = True
stderr_thread.start()

#loop until end of command line
while running:
    #get process status
    p.poll()

    #read outputs and send message
    if client is not None:
        stdout = None
        stderr = None
        try:
            stdout = stdout_queue.get_nowait()
        except:
            pass
        try:
            stderr = stderr_queue.get_nowait()
        except:
            pass

        #send output
        send_output(stdout, True)
        send_output(stderr, False)

    else:
        #no client connected, stop processing command
        logger.debug('Client disconnected. Stop processing.')
        break

    #check end of command
    if p.returncode is not None:
        #command terminated
        return_code = p.returncode
        logger.debug(u'Command terminated with return code %d' % return_code)
        break
    
    #pause
    time.sleep(0.10)

#make sure command is killed
try:
    if sys.platform == 'win32':
        subprocess.Popen(u'taskkill /PID %s /F > nul 2>&1' % pid, shell=True)
    else:
        subprocess.Popen(u'/usr/bin/pkill -9 -P %s 2> /dev/null' % pid, shell=True)

except:
    pass
    
#close socket
if client is not None:
    client.close()

#exit with user command return code
sys.exit(return_code)

