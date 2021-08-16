import argparse

import pytest

from src import cli


@pytest.mark.parametrize(
    "args, exp_output",
    [
        (
            ["--criteria", "subtree-count", "--file", "/path/file"],
            argparse.Namespace(criteria="subtree-count", file="/path/file"),
        ),
        (
            ["--criteria", "subtree-maxdepth", "--file", "/path/file"],
            argparse.Namespace(criteria="subtree-maxdepth", file="/path/file"),
        ),
        (
            ["--criteria", "subtree-average-value", "--file", "/path/file"],
            argparse.Namespace(criteria="subtree-average-value", file="/path/file"),
        ),
    ],
)
def test_correct_args(args, exp_output) -> None:
    parsed_args = cli.parse_cli_args(args)
    assert parsed_args == exp_output


@pytest.mark.parametrize(
    "args",
    [
        ["--criteria", "subtree-coount", "--file", "/path/file"],
        ["--criterials", "subtree-maxdepth", "--file", "/path/file"],
        ["--criteria", "subtree-average-value", "--files", "/path/file"],
        ["--criteria", "subtree-average-value", "--file", "/path/file", "--foo"],
    ],
)
def test_inorrect_args(args) -> None:
    with pytest.raises(ValueError):
        cli.parse_cli_args(args)
