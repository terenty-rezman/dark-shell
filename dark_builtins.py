import os

built_ins = {
    # dict of shell built-ins
    # filled through @builtin decorator
    # e.g.
    # 'exit': exit_builtin
}


class ExitRequest(Exception):
    pass


def builtin(name: str):
    """decorator - makes decorated func to be registered as shell built in with name 'name'"""
    def decorator(builtin_fcn):
        built_ins[name] = builtin_fcn
        return builtin_fcn

    return decorator


@builtin("exit")
def exit(args):
    raise ExitRequest


@builtin("cd")
def cd(args):
    if(len(args) > 1):
        os.chdir(args[1])

    print(os.getcwd())


def is_builtin(cmd):
    return cmd in built_ins


def call(args):
    builtin = built_ins[args[0]]
    return builtin(args)
