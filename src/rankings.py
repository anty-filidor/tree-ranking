import logging
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple

import networkx as nx
import numpy as np

from .tree import find_sub_trees

log = logging.getLogger(__name__)


def compute_ranking(tree: nx.DiGraph, method: str) -> List[Tuple[str, int]]:
    """
    Ranking creator that delegates computations depending on value of the method.

    :param tree: tree to compute ranking for
    :param method: method of computation

    :return: for each color a tuple with its name and ranking value; containerised all
        into the list sorted by value of ranking
    """
    if method == "subtree-count":
        return _compute_subtree_count(tree)
    elif method == "subtree-maxdepth":
        return _compute_subtree_max_depth(tree)
    elif method == "subtree-average-value":
        return _compute_subtree_average_value(tree)

    raise ValueError(f"Computation method {method} unknown!")


def prepare_result(rollup_method: Callable = lambda x: x) -> Callable:
    """
    Decorates result returned by delegate function by custom sorting.

    :param rollup_method: method to concatenate results for one color

    :return: decorated function that computes the ranking
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def _func_wrapper(*args: Any, **kwargs: Any) -> List[Tuple[str, int]]:
            pre_result = func(*args, **kwargs)
            return sorted(
                [(k, rollup_method(v)) for k, v in pre_result.items()],
                key=lambda x: (-1 * x[1], x[0]),
            )

        return _func_wrapper

    return decorator


@prepare_result()
def _compute_subtree_count(tree: nx.DiGraph) -> Dict[str, int]:
    """Compute ranking of tree basing of count of subtrees with the same color."""
    metric: Dict[str, int] = {}
    for sub_tree_nodes in find_sub_trees(tree):

        color = tree.nodes[sub_tree_nodes.pop()]["color"]
        if metric.get(color) is None:
            metric[color] = 1
        else:
            metric[color] += 1

    return metric


@prepare_result()
def _compute_subtree_max_depth(tree: nx.DiGraph) -> Dict[str, int]:
    """Compute ranking of tree basing on a max depth among subtrees of the same color."""
    metric: Dict[str, int] = {}
    for sub_tree_nodes in find_sub_trees(tree):

        sub_tree = nx.subgraph(tree, sub_tree_nodes)
        depth = max(nx.shortest_path_length(sub_tree, min(sub_tree_nodes)).values()) + 1

        color = tree.nodes[sub_tree_nodes.pop()]["color"]
        if metric.get(color) is None:
            metric[color] = depth
        else:
            metric[color] = max(depth, metric[color])

    return metric


@prepare_result(rollup_method=lambda x: int(np.average(x)))
def _compute_subtree_average_value(tree: nx.DiGraph) -> Dict[str, List[int]]:
    """Compute ranking of tree basing on a avg value of subtrees with the same color."""
    metric: Dict[str, List[int]] = {}
    for sub_tree_nodes in find_sub_trees(tree):

        sub_tree_value = sum([tree.nodes[n]["value"] for n in sub_tree_nodes])

        color = tree.nodes[sub_tree_nodes.pop()]["color"]
        if metric.get(color) is None:
            metric[color] = [sub_tree_value]
        else:
            metric[color].append(sub_tree_value)

    return metric
