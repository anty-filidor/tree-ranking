import pathlib
import logging
import pandas as pd
import networkx as nx
import numpy as np
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

log = logging.getLogger(__name__)


def read_tree(tree_path: pathlib.Path, draw: bool) -> nx.Graph:
    """
    Reads tree stored in the csv to the NetworkX Graph.

    :param tree_path: path to the csv
    :param draw: a flag - if true tree will be displayed

    :return: the NetworkX Graph
    """
    if not tree_path.exists():
        raise FileNotFoundError(f"Given path \"{tree_path}\" is not valid")

    tree_df = pd.read_csv(tree_path, sep=';', encoding='utf-8')

    columns_exp = {'color', 'value', 'id', 'parent_id'}
    if not columns_exp.issubset(tree_df.columns):
        raise ValueError(
            f"File \"{tree_path}\" is not valid (should contain {columns_exp})"
        )

    tree_nx = nx.Graph()
    for _, row in tree_df.iterrows():
        tree_nx.add_node(int(row['id']), color=row['color'], value=row['value'])
        if not np.isnan(row['parent_id']):
            tree_nx.add_edge(int(row['parent_id']), int(row['id']))

    if draw:
        draw_tree(tree_nx)

    return tree_nx


# TODO - add docstring
def draw_tree(tree):
    values = [tree.nodes[node]['color'] for node in tree.nodes()]
    pos = graphviz_layout(tree, prog="dot")
    nx.draw(tree, pos, with_labels=True, cmap=plt.get_cmap('viridis'), node_color=values)
    pos_attrs = {node: (coords[0]-10, coords[1]+10) for node, coords in pos.items()}
    node_labels = nx.get_node_attributes(tree, 'value')
    custom_node_attrs = {node: f"(val {attr})" for node, attr in node_labels.items()}
    nx.draw_networkx_labels(tree, pos_attrs, labels=custom_node_attrs, font_size=8)
    plt.show()
