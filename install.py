#!/usr/bin/env python3

"""
installs dark shell as default on your system for current user
linux only
"""

import distutils.util
import getpass
import os
import subprocess
from pathlib import Path


USER_SHELL_BCKUP_DIR = ".user_shell_bckups"


class AlreadyExists(Exception):
    pass


class NotInstalled(Exception):
    pass


def query_yes_no(question):
    while True:
        try:
            resp = input(question).strip().lower()
            return distutils.util.strtobool(resp)
        except ValueError:
            return False


def get_user_name():
    user_name = getpass.getuser()

    if not user_name:
        raise Exception("cannot get user")

    return user_name


def get_user_shell():
    user_shell = os.environ.get("SHELL")
    if not user_shell:
        raise Exception("cannot get $SHELL")
    return user_shell


def do_install():
    base_path = os.path.dirname(__file__)
    base_path = Path(base_path).resolve()  # get absolute path

    backup_dir = os.path.join(base_path, USER_SHELL_BCKUP_DIR)

    if not os.path.exists(backup_dir):
        os.mkdir(USER_SHELL_BCKUP_DIR)

    user_name = get_user_name()

    bckup_file_name = os.path.join(USER_SHELL_BCKUP_DIR, user_name)

    if os.path.isfile(bckup_file_name):
        raise AlreadyExists

    user_shell = get_user_shell()

    dark_path = os.path.join(base_path, 'dark.py')
    dark_path = Path(dark_path).resolve()  # get absolute path

    add_shell_command = ["sudo", "add-shell", dark_path]
    print("executing:", "\n", *add_shell_command)
    result = subprocess.run(add_shell_command)

    if result.returncode != 0:
        raise Exception("cannot add dark to /etc/shells")

    change_shell_command = ["chsh", "-s", dark_path]
    print("executing:", "\n", *change_shell_command)
    result = subprocess.run(change_shell_command)

    if result.returncode != 0:
        raise Exception("cannot set dark as default shell")

    with open(bckup_file_name, "w") as file:
        file.write(user_shell)


def install():
    try:
        yes = query_yes_no("set dark shell as your default? [y/n]: ")
        if yes:
            do_install()
            print("\ndark is successfully installed!",
                  "use uninstall.py to uninstall")
        else:
            print("canceled")
    except KeyboardInterrupt:
        print("\ncanceled")
    except AlreadyExists:
        print("\ndark is already installed")


def do_uninstall():
    base_path = os.path.dirname(__file__)
    base_path = Path(base_path).resolve()  # get absolute path

    backup_dir = os.path.join(base_path, USER_SHELL_BCKUP_DIR)

    if not os.path.exists(backup_dir):
        raise NotInstalled

    user_name = get_user_name()

    bckup_file_name = os.path.join(USER_SHELL_BCKUP_DIR, user_name)

    if not os.path.isfile(bckup_file_name):
        raise NotInstalled

    with open(bckup_file_name, "r") as file:
        user_shell = file.read()

    if not user_shell:
        raise Exception("cannot restore shell for user", user_name)

    restore_shell_command = ["chsh", "-s", user_shell]
    print("executing:", "\n", *restore_shell_command)
    result = subprocess.run(restore_shell_command)

    if result.returncode != 0:
        raise Exception("could not chsh for user", user_name)

    os.remove(bckup_file_name)


def uninstall():
    try:
        yes = query_yes_no("restore your original shell? [y/n]: ")
        if yes:
            do_uninstall()
            print("\ndefault shell restored")
        else:
            print("canceled")

    except NotInstalled:
        print("\ndark is not installed")


if __name__ == "__main__":
    install()
