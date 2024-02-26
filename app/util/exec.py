import subprocess as sp
import logging as log


def run_shell(s):

    try:

        log.debug("run_shell: %s", s)

        with sp.Popen(s, stdout=sp.PIPE, stderr=sp.PIPE, shell=True) as cmd:

            log.debug("cmd: %s", cmd)

            _stdout, _stderr = cmd.communicate()

            log.debug("cmd run: output: %s, %s", _stdout, _stderr)

            if cmd.returncode != 0:
                return (1, _stdout + _stderr)

            return (0, _stdout)

    except Exception as e:
        log.error("ERROR: %s", e)
        return (1, str(e))
