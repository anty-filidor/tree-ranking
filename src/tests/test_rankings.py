import pytest
from src import tree, rankings
from pathlib import Path
from unittest import mock
import networkx as nx

tree_01 = tree.read_tree(Path("examples/tree_01.csv"), False)
tree_02 = tree.read_tree(Path("examples/tree_02.csv"), False)
tree_03 = tree.read_tree(Path("examples/tree_03.csv"), False)


@pytest.mark.parametrize(
    "method, func_called",
    [
        ("subtree-count", "src.rankings._compute_subtree_count"),
        ("subtree-maxdepth", "src.rankings._compute_subtree_max_depth"),
        ("subtree-average-value", "src.rankings._compute_subtree_average_value"),
    ]
)
def test_compute_ranking(method, func_called):
    with mock.patch(func_called) as mocked_delegate:
        rankings.compute_ranking(nx.DiGraph(), method)
        mocked_delegate.assert_called_once()




@pytest.mark.parametrize(
    "testing_tree, exp_result",
    [
        (
                tree_01,
                [('blue', 2), ('green', 1), ('yellow', 1)]
        ),
        (
                tree_02,
                [('orange', 3), ('red', 3), ('green', 2), ('pink', 2), ('blue', 1)]
        ),
        (
                tree_03,
                [('red', 2), ('black', 1), ('blue', 1), ('green', 1), ('orange', 1), ('purple', 1), ('yellow', 1)]
        ),
    ]
)
def test__compute_subtree_count(testing_tree, exp_result):
    real_res = rankings._compute_subtree_count(testing_tree)
    assert exp_result == real_res


@pytest.mark.parametrize(
    "testing_tree, exp_result",
    [
        (
                tree_01,
                [('yellow', 3), ('blue', 2), ('green', 1)]
        ),
        (
                tree_02,
                [('blue', 5), ('red', 3), ('green', 2), ('orange', 2), ('pink', 1)]
        ),
        (
                tree_03,
                [('black', 1), ('blue', 1), ('green', 1), ('orange', 1), ('purple', 1), ('red', 1), ('yellow', 1)]
        ),
    ]
)
def test__compute_subtree_max_depth(testing_tree, exp_result):
    real_res = rankings._compute_subtree_max_depth(testing_tree)
    assert exp_result == real_res


@pytest.mark.parametrize(
    "testing_tree, exp_result",
    [
        (
                tree_01,
                [('green', 400), ('yellow', 300), ('blue', 150)]
        ),
        (
                tree_02,
                [('blue', 750), ('red', 396), ('orange', 266), ('green', 225), ('pink', 160)]
        ),
        (
                tree_03,
                [('yellow', 90), ('purple', 70), ('black', 40), ('orange', 35), ('red', 35), ('blue', 10), ('green', 10)]
        ),
    ]
)
def test__compute_subtree_average_value(testing_tree, exp_result):
    real_res = rankings._compute_subtree_average_value(testing_tree)
    assert exp_result == real_res
