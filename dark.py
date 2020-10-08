#!/usr/bin/env python3

import os
import subprocess
import shlex

import dark_shell.colors as c
import dark_shell.builtins as dark_builtins

PROMPT = f"{c.PINK}> {c.GREY}"


def print_wellcome_msg():
    import getpass
    import socket

    username = getpass.getuser()
    hostname = socket.gethostname()

    msg = f"{c.DARK}{username}{c.PINK}@{c.DARK}{hostname}{c.PINK} > {c.BLACK}dark shell"
    print(msg)
    print(f"{c.DARK}" + os.getcwd())


# for python exec()
python_exec_globals = {"PROMPT": PROMPT}
python_exec_locals = {}


def exec_as_python_code(code):
    try:
        result = eval(code, python_exec_globals, python_exec_locals)
        if(result is not None):
            print(result)
    except Exception:
        exec(code, python_exec_globals, python_exec_locals)


def dark_execute(args, raw_command_line):
    if not len(args):
        return

    if(dark_builtins.is_builtin(args[0])):
        return dark_builtins.call(args)
    else:
        try:
            subprocess.run(args)
        except FileNotFoundError:
            exec_as_python_code(raw_command_line)

    return False


def shell_loop():
    while True:
        try:
            command_line = input(PROMPT)
            args = shlex.split(command_line)

            dark_execute(args, command_line)

        except dark_builtins.ExitRequest:
            print(f"{c.NONE}")
            break
        except KeyboardInterrupt:
            print("")
        except Exception as ex:
            print(f"{c.RED}{ex}{c.NONE}")


if __name__ == "__main__":
    print_wellcome_msg()
    shell_loop()
