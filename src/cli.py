import argparse
from typing import List
import logging


def init_logger() -> None:
    """Initialises logger."""
    ch = logging.StreamHandler()

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)-8s] [%(levelname)s] msg: "%(message)s"',
        datefmt="%H:%M:%S",
        handlers=[ch],
    )


def parse_cli_args(cli_args: List[str]) -> argparse.Namespace:
    """
    Parses cli arguments for calling project from CLI.

    :param cli_args: console arguments

    :return:
    """
    parser = argparse.ArgumentParser(
        description="I'm running a Tree Ranker."
    )
    parser.add_argument(
        "--criteria",
        help="determines a way that ranking is computed",
        required=True,
        choices=['subtree-count', 'subtree-maxdepth', 'subtree-average-value']
    )
    parser.add_argument(
        "--file",
        help="path to the cvs file with tree defined",
        required=True,
    )

    return parser.parse_args(cli_args)
