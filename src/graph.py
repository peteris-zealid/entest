from src.dependency_decorator import TEST_ROOT, TestCase


def mermaid_edges(node: TestCase):
    parent_name = node.name()
    return [f"{parent_name} --> {child.name()};" for child in node.children]


def graph(root=TEST_ROOT):
    visited_nodes = set()
    unvisited_nodes = {root}
    edges = []
    while unvisited_nodes:
        node = unvisited_nodes.pop()
        visited_nodes.add(node)
        unvisited_nodes.update([child for child in node.children if child not in visited_nodes])
        edges.extend(mermaid_edges(node))

    return "graph TD;\n" + "\n".join(edges)
