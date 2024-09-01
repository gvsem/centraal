
def ssh_run_cmds(client, cmds):
    """
    Run sequence of commands using ssh client and print its output
    to stdout and stderr. If one of commands fails (exit code is not zero),
    execution proceeds, so there is no pipe semantics.
    """
    for cmd in cmds:
        _stdin, _stdout, _stderr = client.exec_command(cmd)
        stdout = _stdout.read().decode()
        stderr = _stderr.read().decode()
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
