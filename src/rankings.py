import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Tuple, Set, Dict
from dataclasses import dataclass
import logging

from .tree import draw_tree, find_sub_trees

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


def _compute_subtree_count(tree: nx.DiGraph) -> List[Tuple[str, int]]:
    """Computes ranking of tree basing of count of subtrees with the same color."""
    metric = {}
    for sub_tree in find_sub_trees(tree):
        color = tree.nodes[sub_tree.pop()]['color']
        if metric.get(color) is None:
            metric[color] = 1
        else:
            metric[color] += 1

    return prepare_result(metric)


def _compute_subtree_max_depth(tree: nx.DiGraph) -> List[Tuple[str, int]]:
    return 1


def _compute_subtree_average_value(tree: nx.DiGraph) -> List[Tuple[str, int]]:
    return 2


def prepare_result(pre_result: Dict[str, int]) -> List[Tuple[str, int]]:
    return sorted([(k, v) for k, v in pre_result.items()], key=lambda x: (-1*x[1], x[0]))
