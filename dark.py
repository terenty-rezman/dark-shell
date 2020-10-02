#!/usr/bin/env python3

import os
import subprocess
import shlex

import dark_shell.colors as c
import dark_shell.builtins as dark_builtins

PROMPT = f"{c.PINK}> {c.GREY}"

WELLCOME_MSG = f"""
{c.DARK} welcome to {c.BLACK}dark {c.DARK}shell
"""

# for python exec()
python_exec_globals = {"PROMPT": PROMPT}
python_exec_locals = {}


def exec_as_python_code(code):
    result = exec(code, python_exec_globals, python_exec_locals)
    if(result):
        print(result)


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
    print(WELLCOME_MSG)
    shell_loop()
