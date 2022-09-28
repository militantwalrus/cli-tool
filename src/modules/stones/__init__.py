import argparse
import sys
from typing import Any, List, Tuple

from src.command import BaseCommand, MutuallyExclusiveOptions, ToolCommand
from src.util import do_something


class Commands(BaseCommand):
    """
    Stones module
    """

    USAGE = """cli-tool stones [command] [options...]

Available commands
"""

    def __init__(self, opts: argparse.Namespace) -> None:
        """
        Constructor
        """
        self.opts = opts
        self.USAGE += "".join([f"    {fn}\n" for fn in self.command_methods()])

        self.arg_parser = argparse.ArgumentParser(usage=self.USAGE)
        self.arg_parser.add_argument("--debug", action="store_true", help="Turn on debug logging")
        self.arg_parser.add_argument("-e", action="store", help="something defined by -e")
        self.arg_parser.add_argument("--guitar", nargs="?", action="store")

        super().__init__()  # must come after self.arg_parser is assigned

    @ToolCommand
    @MutuallyExclusiveOptions(["--guitar", "--drums"])
    def keith(self) -> None:
        self.arg_parser.add_argument("--drums", nargs="?", action="store")
        self.cond_do_help("keith")

        opts, args = self.arg_parser.parse_known_args(sys.argv[3:])  # skip [cli-tool mod cmd]
        print(f"Keith called with opts: {opts}  args: {args}")
        do_something()

    @ToolCommand
    def mick(self) -> None:
        self.cond_do_help("mick")

        opts, args = self.arg_parser.parse_known_args(sys.argv[3:])  # skip [cli-tool mod cmd]
        print(f"Mick called with opts: {opts}  args: {args}")
        do_something()

    def brian(self) -> None:
        """
        Test that it doesn't work without @ToolCommand
        """
        opts, args = self.arg_parser.parse_known_args(sys.argv[3:])  # skip [cli-tool mod cmd]
        print(f"Brian called with opts: {opts}  args: {args}")
