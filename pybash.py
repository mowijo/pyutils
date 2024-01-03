import subprocess
import shlex

class Result:

    def __init__(self):
        self.stdErr = ""
        self.stdOut = ""
        self.returnCode = -1

    def __bool__(self):
        return self.returnCode == 0

    def __str__(self):
        if self.returnCode == 0:
            return self.stdOut
        else:
            return self.stdErr

class x__command_failed_error(Exception):
    pass


def x__parameters__to__command__array(string):
    commands = []

    for part in string.split("|"):
        commands.append(shlex.split(part))

    return commands



def x(command):

    commandWithArguments = x__parameters__to__command__array(command)
    result = Result()

    prev_proc = subprocess.Popen(commandWithArguments[0], stdout=subprocess.PIPE)

    for args in commandWithArguments[1:]:

       proc = subprocess.Popen(args, stdin=prev_proc.stdout, stdout=subprocess.PIPE)
       prev_proc.stdout.close()
       prev_proc = proc

    (result.stdOut, result.stdErr) = prev_proc.communicate()

    result.returnCode = prev_proc.returncode
    if result.stdOut:
        result.stdOut = result.stdOut.decode("utf-8")
    else:
        result.stdOut = ""

    if result.stdErr:
        result.stdErr = result.stdErr.decode("utf-8")
    else:
        result.stdErr = ""

    return result

