from  WinCmdRunner import *
from CmdRunner import CommandProcException
import Queue

def getCmdObj (cmd, errmsgfilter=None, nonerrmsgfilter=None, nonerrcodefilter=None):
    cmd = '('+cmd+')'
    return (cmd,(errmsgfilter, nonerrmsgfilter, nonerrcodefilter))

def runCommandsInSequence(cmdlist, logdir=None, cwd=None, waitcmdprompt=False):
    """
    :param cmdlist: list of command string to be executed on the windows command prompt.
    :param logdir: log directory path 
    :param cwd:  current working directory.
    :param waitcmdprompt: makes the windows cmd prompt to stay on.
    :return: 
    """
    for cmd in cmdlist:
        cmdobj = getCmdObj(cmd)
        p = WinCmdRunner(command=cmdobj, cwd=cwd, daemonprocess=False, waitcmdprompt=waitcmdprompt, logdir=logdir)
        p.start()
        p.wait()


def runCommandsInParallel(cmdlist, logdir=None, cwd=None, daemon=False, waitcmdprompt=False):
    """
    :param cmdlist: list of command string to be executed on the windows command prompt.
    :param logdir: log directory path 
    :param cwd:  current working directory.
    :param daemon: runs the commands in background.
    :param waitcmdprompt: makes the windows cmd prompt to stay on.
    :return:
    """
    processlist = []
    errormsgs = ""
    for cmd in cmdlist:
        cmdobj = getCmdObj(cmd)
        p = WinCmdRunner(command=cmdobj, cwd=cwd, daemonprocess=daemon, waitcmdprompt=waitcmdprompt, logdir=logdir)
        p.start()
        processlist.append(p)

    if daemon == False:
        for process in processlist:
            try:
                process.wait()
            except Exception as e:
                errormsgs += str(e)

    if len(errormsgs) > 0:
        raise CommandProcException(errormsgs)


def runMethodsInParallel(*methods):
    threads = []
    exception_queue = Queue.Queue()

    for method in methods:
        p = WinCmdRunner(command=method, exceptionqueue=exception_queue)
        p.start()
        threads.append(p)

    for thread in threads:
        thread.wait()

    errormsg = ''

    while not exception_queue.empty():
        queuederrmsg = exception_queue.get()
        errormsg += queuederrmsg

    if len(errormsg) > 0:
        raise CommandProcException(errormsg)