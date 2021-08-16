"""Contain functions that compute rankings of trees."""
import logging
import pathlib
import sys

from src import cli, rankings, tree

if __name__ == "__main__":

    cli.init_logger()
    log = logging.getLogger(__name__)
    log.info("Logging utility initialised successfully!")

    parsed_cli_args = cli.parse_cli_args(sys.argv[1:])
    path_to_csv = pathlib.Path(parsed_cli_args.file)
    computation_method = parsed_cli_args.criteria
    log.info(f"Passed path with tree file as: {path_to_csv}.")
    log.info(f"Passed method of ranking computation as: {computation_method}.")

    tree = tree.read_tree(path_to_csv, False)
    log.info("Tree has been read successfully!")

    rank = rankings.compute_ranking(tree, computation_method)
    log.critical(f"Ranking {computation_method} computed on tree {path_to_csv}")
    log.critical(rank)
