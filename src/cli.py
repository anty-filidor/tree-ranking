"""Contains functions that facilitate command line usage of this program."""
import argparse
import logging
import sys
from typing import List, NoReturn


class MyArgumentParser(argparse.ArgumentParser):
    """This class has been implemented just to raise ValueError instead of SystemExit."""

    def error(self, message: str) -> NoReturn:
        """Raises ValueError when arguments are incorrect."""
        self.print_help(sys.stderr)
        raise ValueError("%s: error: %s\n" % (self.prog, message))


def parse_cli_args(cli_args: List[str]) -> argparse.Namespace:
    """
    Parses cli arguments for calling project from CLI.

    :param cli_args: console arguments

    :return: parsed arguments
    """
    parser = MyArgumentParser(description="I'm running a Tree Ranker.")
    parser.add_argument(
        "--criteria",
        help="determines a way that ranking is computed",
        required=True,
        choices=["subtree-count", "subtree-maxdepth", "subtree-average-value"],
    )
    parser.add_argument(
        "--file", help="path to the cvs file with tree defined", required=True,
    )

    return parser.parse_args(cli_args)


def init_logger() -> None:
    """Initialises logger."""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)-8s] [%(levelname)s] msg: "%(message)s"',
        datefmt="%H:%M:%S",
    )
