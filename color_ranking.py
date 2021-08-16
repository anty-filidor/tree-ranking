import logging
import pathlib
import sys

from src import cli, tree


if __name__ == "__main__":

    # init logger
    cli.init_logger()
    log = logging.getLogger(__name__)

    # parse cli arguments
    parsed_cli_args = cli.parse_cli_args(sys.argv[1:])
    path_to_csv = pathlib.Path(parsed_cli_args.file)
    computation_method = parsed_cli_args.criteria

    # print out parsed arguments
    log.info(f"Passed path with tree file as: {path_to_csv}")
    log.info(f"Passed method of ranking computation as: {computation_method}")

    # read the tree
    tree.read_tree(path_to_csv)

