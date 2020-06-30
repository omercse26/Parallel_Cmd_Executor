from RunCommands import *
echo = ("echo %s")

def print_message_in_win_cmd(message):
    # echo command to be run on windows cmd prompt.
    echocmd = echo % message

    # Runs the commands in the command list in parallel.
    # waitcmdprompt will make the windows cmd to stay on.
    # In this command, only echo cmd is in the input list.
    runCommandsInParallel([echocmd], waitcmdprompt=True)

print_message_in_win_cmd("Hello World")


