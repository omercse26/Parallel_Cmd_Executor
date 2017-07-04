from CmdRunner import *
echo = ("echo %s")

def print_message_in_win_cmd(message):
    cmdlist = [getCmdObj(echo % message)] * 10
    runCommandsInParallel(cmdlist, waitcmdprompt=True)

print_message_in_win_cmd("Hello World")


