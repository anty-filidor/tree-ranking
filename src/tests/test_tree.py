from pathlib import Path

import pytest

from src import tree


@pytest.mark.parametrize(
    "path", [Path("path/to/non/existing/file.csv"), Path("another/path.csv")],
)
def test_read_tree_file_not_found(path):
    with pytest.raises(FileNotFoundError):
        tree.read_tree(path, False)


def test_read_tree_file_corrupted():
    corrupted_file_path = Path("examples/tree_corrupted.csv")
    with pytest.raises(ValueError):
        tree.read_tree(corrupted_file_path, False)
