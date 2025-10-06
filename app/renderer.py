from graphviz import Digraph
from typing import Dict, Any
from app.tree_types import AttackTree

def render_graph(tree: AttackTree, fmt: str = "png") -> bytes:
    g = Digraph(format=fmt)
    # root node
    g.node("root", tree.goal, shape="box", style="filled")

    # add nodes
    for node in tree.nodes:
        label = node.text
        # include type or metrics if present
        extras = []
        if node.probability is not None:
            extras.append(f"P={node.probability}")
        if node.cost is not None:
            extras.append(f"C={node.cost}")
        if extras:
            label = f"{label}\\n({' ,'.join(extras)})"
        g.node(node.id, label)

    # edges
    # Connect root to top-level nodes not referenced as child by any node (safe fallback)
    child_ids = {c for n in tree.nodes for c in n.children}
    top_nodes = [n.id for n in tree.nodes if n.id not in child_ids]
    for nid in top_nodes:
        g.edge("root", nid)

    for node in tree.nodes:
        for c in node.children:
            g.edge(node.id, c)

    return g.pipe()
