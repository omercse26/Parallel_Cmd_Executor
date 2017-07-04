from CmdRunner import CmdRunner
import subprocess

class WinCmdRunner(CmdRunner):
    def __init__(self, command=('echo hello', None), logdir=None, cwd=None, daemonprocess=False,
                 waitcmdprompt=False, exceptionqueue=None):
        super(WinCmdRunner, self).__init__(command, logdir, cwd, daemonprocess, waitcmdprompt, exceptionqueue)

    def getTargetCommand(self, curr_working_dir, waitcmdprompt):
        def targetCommand():
            prompt = '/k' if waitcmdprompt else '/c'
            title = self.command.replace('"', '')

            if self.daemonprocess == False:
                runcmd = 'start "' + title + '" /wait cmd ' + prompt + ' "' + self.command + ' 2>' + self.errmsgfile + ' & call echo %^errorLevel% > ' + self.errcodefile + '"'
            else:
                runcmd = 'start "' + title + '" /wait cmd ' + prompt + ' "' + self.command + '"'

            h = subprocess.Popen(runcmd, shell=True, cwd=curr_working_dir)
            self.processhandle.append(h)

        return targetCommand