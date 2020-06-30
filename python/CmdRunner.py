import subprocess
import threading
import os
import Queue
import datetime

class CmdRunner(threading.Thread):
        def __init__(self, command=('echo hello', None), logdir=None, cwd=None, daemonprocess=False,
                     waitcmdprompt=False, exceptionqueue=None):

            self.exceptionqueue = exceptionqueue

            if hasattr(command, '__call__') == True:
                self.command = command
                super(CmdRunner, self).__init__(target=self.command)

            elif command[0] is not None and isinstance(command[0], basestring):

                self.command, self.errorfilter = command

                stripcommand = ''.join(e for e in self.command if e.isalnum())
                stripcommand = stripcommand[:200] if len(stripcommand) > 200 else stripcommand

                if logdir is None:
                    logdir = os.getcwd()

                self.daemonprocess = daemonprocess
                self.processhandle = []

                logtimestamp = os.path.join('log', datetime.datetime.now().strftime("%Y%m%d"))
                self.errmsgdir = os.path.join(logdir, os.path.join(logtimestamp, 'err'))
                self.errcodedir = os.path.join(logdir, os.path.join(logtimestamp, 'ret'))

                if not os.path.exists(self.errmsgdir):
                    os.makedirs(self.errmsgdir)

                if not os.path.exists(self.errcodedir):
                    os.makedirs(self.errcodedir)

                self.errmsgfile = os.path.join(self.errmsgdir, stripcommand + ".err")
                self.errcodefile = os.path.join(self.errcodedir, stripcommand + ".ret")

                t = self.getTargetCommand(cwd, waitcmdprompt)
                super(CmdRunner, self).__init__(target=t)

            else:
                raise CommandProcException("Invalid Command to execute")

        def run(self):
            try:
                self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
                if hasattr(self.command, '__call__') == False and self.daemonprocess == False:
                    self.processhandle[0].wait()
            except Exception as e:
                if self.exceptionqueue is not None:
                    self.exceptionqueue.put(str(e))

        def wait(self):
            self.join()
            if hasattr(self.command, '__call__') == False:
                errmsg, errcode = self.getErrMsgAndErrCode()
                if len(errmsg) > 0 or errcode != 0:
                    raise CommandProcException((self.command, errmsg, errcode))

        def getTargetCommand(self, curr_working_dir, waitcmdprompt):
            raise NotImplementedError("Implement target method")

        def getErrMsgAndErrCode(self):

            errlist, nonerrlist, nonerrcode = self.errorfilter if self.errorfilter is not None else (None, None, None)

            if errlist is not None:
                errlist = [i.lower() for i in errlist if i is not None and len(i) > 0]

            if nonerrlist is not None:
                nonerrlist = [i.lower() for i in nonerrlist if i is not None and len(i) > 0]

            def IsErrorMessage(line):

                if nonerrlist is not None:
                    for nonerrmsg in nonerrlist:
                        if nonerrmsg in line.lower():
                            return False

                if errlist is not None:
                    for errmsg in errlist:
                        if errmsg in line.lower():
                            return True
                    return False

                return True

            errmsg = ''

            with open(self.errmsgfile) as f:
                for line in f:
                    if IsErrorMessage(line) == True:
                        errmsg += line

            errcode = 0
            with open(self.errcodefile) as f:
                try:
                    errcode = int(f.read())
                except ValueError:
                    errcode = 0

            if nonerrcode is not None and errcode in nonerrcode:
                errcode = 0

            return errmsg, errcode

class CommandProcException(Exception):
    def __init__(self, exceptiontuple):
        self.errmsg = ''
        if isinstance(exceptiontuple, basestring):
            self.errmsg += exceptiontuple
        else:
            self.errmsg += '=====================================================================\n'
            self.errmsg += 'Error in command: ' + exceptiontuple[0]
            self.errmsg += '\nError Message:\n' + exceptiontuple[1].rstrip('\n')
            self.errmsg += '\nError Code: ' + str(exceptiontuple[2]) + '\n'
            self.errmsg += '=====================================================================\n'

    def __str__(self):
        return self.errmsg