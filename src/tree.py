import logging
import pathlib
from typing import List, Optional, Set

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from networkx.drawing.nx_pydot import graphviz_layout

log = logging.getLogger(__name__)


def read_tree(tree_path: pathlib.Path, draw: bool) -> nx.DiGraph:
    """
    Reads tree stored in the csv to the NetworkX DiGraph.

    :param tree_path: path to the csv
    :param draw: a flag - if true tree will be displayed

    :return: the NetworkX Graph
    """
    if not tree_path.exists():
        raise FileNotFoundError(f"Given path '{tree_path}' is not valid")

    tree_df = pd.read_csv(tree_path, sep=";", encoding="utf-8")

    columns_exp = {"color", "value", "id", "parent_id"}
    if not columns_exp.issubset(tree_df.columns):
        raise ValueError(
            f"File '{tree_path}' is not valid (should contain {columns_exp})"
        )

    tree_nx = nx.DiGraph()
    for _, row in tree_df.iterrows():
        tree_nx.add_node(int(row["id"]), color=row["color"], value=row["value"])
        if not np.isnan(row["parent_id"]):
            tree_nx.add_edge(int(row["parent_id"]), int(row["id"]))

    if draw:
        draw_tree(tree_nx, None)

    return tree_nx


def find_sub_trees(tree: nx.DiGraph) -> List[Set[int]]:
    """
    Finds subtrees in the tree by the criteria of similar color.

    :param tree: tree to find subtrees for

    :return: a list of sets of nodes from the tree that create subtrees
    """
    _tree = tree.copy()

    edges_to_remove = [
        edge
        for edge in tree.edges()
        if tree.nodes[edge[0]]["color"] != tree.nodes[edge[1]]["color"]
    ]
    log.debug(f"Found edges to remove as: {edges_to_remove}")
    _tree.remove_edges_from(edges_to_remove)

    sub_trees_nodes = list(nx.weakly_connected_components(_tree))
    log.info(f"Detected following subtrees: {sub_trees_nodes}")

    # uncomment to get visualisations
    # draw_tree(tree, None)
    # draw_tree(_tree, None)

    return sub_trees_nodes


def draw_tree(tree: nx.DiGraph, file_path: Optional[pathlib.Path]) -> None:
    """
    Draws a tree depicting colors of nodes, labels and direction of connections.

    :param tree: a tree to display
    :param file_path: an optional path to the file for saving the image

    :return: None
    """
    nodes_position = graphviz_layout(tree, prog="dot")
    attrs_position = {
        node: (coords[0] - 10, coords[1] + 10) for node, coords in nodes_position.items()
    }

    node_labels = nx.get_node_attributes(tree, "value")
    node_values = {node: f"(val {attr})" for node, attr in node_labels.items()}
    node_colors = [tree.nodes[node]["color"] for node in tree.nodes()]

    nx.draw(
        tree,
        nodes_position,
        with_labels=True,
        cmap=plt.get_cmap("viridis"),
        node_color=node_colors,
    )
    nx.draw_networkx_labels(tree, attrs_position, labels=node_values, font_size=8)

    if file_path is None:
        plt.show()
    else:
        plt.savefig(file_path)
