import argparse
import importlib
import sys
from typing import List, Optional


class BaseCommand:
    """
    """
    def __init__(self) -> None:
        """
        Constructor
        -- if a command was not specified, possibly run print_help()
        """
        if not self.opts.command:
            self.cond_do_help()  # no arg - that's for a command name

    def cond_do_help(self, command_name: Optional[str] = None) -> None:
        """
        Run argparse.print_help() if -h or --help was specified
        """
        if command_name:
            self.arg_parser.usage = self.arg_parser.usage.replace("[command]", command_name)

        if "-h" in sys.argv[2:] or "--help" in sys.argv[2:]:
            self.arg_parser.print_help()
            sys.exit()

    @classmethod
    def command_methods(cls: type) -> List[str]:
        """
        Find all the functions in the module class decorated by @ToolCommand
        """
        ret = []
        for name in dir(cls):
            if hasattr(getattr(cls, name), "_tool_command"):
                ret.append(name)
        return ret


def ToolCommand(fn):
    """
    Tag decorated functions so list_commands() can identify them
    """
    def decorator(self, *args, **kwargs):
        fn(self, *args, **kwargs)
    decorator._tool_command = True
    return decorator


def list_commands(available_module_paths: List[str]):
    """
    Print a listing of available modules and their commands (those decorated with @ToolCommand)
    """
    out = "\nAvailable modules & commands\n\n"
    for ent in available_module_paths:
        sys.path.append(str(ent))
        modname = ent.parts[-1]
        modpath = f"src.modules.{modname}"
        importlib.import_module(modpath)
        cls = getattr(sys.modules[modpath], "Commands", None)
        if not cls:
            continue

        found = cls.command_methods()

        if found:
            out += f"  Module '{modname}' commands:\n"
            for f in found:
                out += f"       {f}\n"

        out += "\n"

    return out


def MutuallyExclusiveOptions(ex_opts):
    """
    specify above a module command like
    @MutuallyExclusiveOptions(["--apples", "--oranges"])
    to indicate that you can't have apples and oranges at the same time
    """
    def decorator(fn):
        def inner(self, *args, **kwargs):
            if isinstance(self.opts, argparse.Namespace):
                have = []
                for o in ex_opts:
                    if o in sys.argv:
                        have.append(o)
                if len(have) > 1:
                    print(f"Mutually exclusive options {have} were used")
                    sys.exit(1)
            fn(self, *args, **kwargs)
        return inner
    return decorator
