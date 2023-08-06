import os, sys
from subprocess import *


def cmd(command, shell=False):
    return check_output(command, shell=shell).decode('utf-8')

try:
    PATH = cmd('git rev-parse --show-toplevel')
    PATH = os.path.dirname(PATH)
except:
    PATH = os.getcwd()

SISTER_PATHS = [os.path.join(PATH, package) for package in os.listdir(PATH)
                if '.' not in package and not 'game' in package.lower()]


def func_iter(func):
    func_name = func.__name__

    def ret(*args):
        for path in SISTER_PATHS:
            os.chdir(path)
            print('\n\n' + func_name.replace('_', ' ') + '-\t' + path)
            try:
                func(*args)
            except BaseException as e:
                pass

    if func.__code__.co_argcount == 0:
        return ret

    def alt():
        ret()

    return alt


def status(echo=True):
    cmd('git fetch origin')
    result = cmd('git status', shell=True)
    if echo:
        print(result)
    return result


def current_branch():
    return cmd('git rev-parse --abbrev-ref HEAD')


@func_iter
def seaborn_install():
    result = cmd('pip install . -U')
    print(result)


@func_iter
def seaborn_debug():
    result = cmd('pip install -e . -U ')
    print(result)


@func_iter
def seaborn_status():
    return status()


@func_iter
def seaborn_commit(*args):
    commit = 'not staged' in status(False)
    if commit:
        print(cmd('git add -A', shell=True))
        print(cmd('git commit -m "%s"' % args[0], shell=True))
    else:
        print('Not committing: Everything up-to-date\n')
    return commit


@func_iter
def seaborn_push():
    print(cmd('git push origin %s'%current_branch(), shell=True))


@func_iter
def seaborn_pull():
    mstr = '*master' in cmd('git branch')
    pull = 'up-to-date' in status(False)
    if mstr and pull:
        print(cmd('git pull origin master'))
