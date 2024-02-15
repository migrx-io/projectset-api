import subprocess as sp


def run_shell(cmd):
    return sp.check_output("{};exit 0".format(cmd),
                           shell=True,
                           stderr=sp.STDOUT).decode('utf-8').strip()
