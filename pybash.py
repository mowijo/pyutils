import subprocess

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



def x(command):

    commandWithArguments = command

    if isinstance(command, str):
        commandWithArguments = command.split()

    result = Result()
    try:
        child= subprocess.run(commandWithArguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result.stdOut = child.stdout.decode('utf-8')
        result.stdErr = child.stderr.decode('utf-8')
        result.returnCode = child.returncode
    except FileNotFoundError:
        result.stdErr = "'"+commandWithArguments[0]+"': No such file or directory"
        result.returnCode = 127

    if result.returnCode != 0:
        if 'setE' in globals():
            if setE:
                print(result.stdErr)
                exit(result.returnCode)

    return result



setE = True
r = x(['ls','-la'])
print(r)
print("-------------------")

