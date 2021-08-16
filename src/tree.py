import pathlib
import logging

log = logging.getLogger(__name__)


def read_tree(tree_path: pathlib.Path) -> None:
    if not tree_path.exists():
        raise FileNotFoundError(f"Given path \"{tree_path}\" is not valid")

