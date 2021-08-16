import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Tuple, Set
from dataclasses import dataclass
import logging

from .tree import draw_tree

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

    raise ValueError(f"Computation method {method} unknown to the program!")


def _compute_subtree_count(tree: nx.DiGraph) -> List[Tuple[str, int]]:

    metric = {}
    for sub_tree in _find_sub_trees(tree):
        color = tree.nodes[sub_tree.pop()]['color']
        if metric.get(color) is None:
            metric[color] = 1
        else:
            metric[color] += 1

    return metric


def _compute_subtree_max_depth(tree: nx.DiGraph) -> List[Tuple[str, int]]:
    return 1


def _compute_subtree_average_value(tree: nx.DiGraph) -> List[Tuple[str, int]]:
    return 2


def _find_sub_trees(tree: nx.DiGraph) -> List[Set[int]]:
    """Finds subtrees in the tree by the criteria of similar color."""
    _tree = tree.copy()

    edges_to_remove = [
        edge for edge in tree.edges() if
        tree.nodes[edge[0]]['color'] != tree.nodes[edge[1]]['color']
    ]
    log.debug(f"Found edges to remove as: {edges_to_remove}")
    _tree.remove_edges_from(edges_to_remove)

    sub_trees = list(nx.weakly_connected_components(_tree))
    log.info(f"Detected following subtrees: {sub_trees}")

    # draw_tree(_tree)
    # draw_tree(tree)

    return sub_trees
