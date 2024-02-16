import subprocess as sp


def run_shell(cmd):
    return sp.check_output(f"{cmd};exit 0", shell=True,
                           stderr=sp.STDOUT).decode('utf-8').strip()
