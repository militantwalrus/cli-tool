import argparse
import sys
from typing import Any, List, Optional, Tuple

from src.command import BaseCommand, ToolCommand
from src.util import do_something


class Commands(BaseCommand):
    """
    Who module
    """

    USAGE = """cli-tool who [command] [options...]

Available commands
"""

    def __init__(self, opts: argparse.Namespace) -> None:
        """
        """
        self.opts = opts
        self.USAGE += "".join([f"    {fn}" for fn in self.command_methods()])

        self.arg_parser = argparse.ArgumentParser(usage=self.USAGE)
        self.arg_parser.add_argument("--debug", action="store_true", help="Turn on debug logging")
        self.arg_parser.add_argument("-e", action="store", help="something defined by -e")
        self.arg_parser.add_argument("--guitar", nargs="?", action="store")

        super().__init__()  # must come after self.arg_parser is assigned

    @ToolCommand
    def roger(self) -> None:
        self.arg_parser.add_argument("--hair", help="Hairstyle")
        self.cond_do_help("roger")

        opts, args = self.arg_parser.parse_known_args(sys.argv[3:])  # skip [cli-tool mod cmd]
        print(f"Roger called with opts: {opts}  args: {args}")
        do_something()

    @ToolCommand
    def pete(self) -> None:
        self.arg_parser.add_argument("--angst", action="store", help="Artistic Angst")
        self.cond_do_help("pete")

        opts, args = self.arg_parser.parse_known_args(sys.argv[3:])  # skip [cli-tool mod cmd]
        print(f"Pete called with opts: {opts}  args: {args}")
        do_something()
