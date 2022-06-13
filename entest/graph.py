from entest.dependency_decorator import TEST_ROOT, TestCase


def mermaid_edges(node: TestCase):
    node_name = node.name()
    test_edges = []
    teardown_edges = []
    for child in node.children:
        if child.run_last:
            teardown_edges.append(f"{node_name} --> {child.name()};")
        else:
            test_edges.append(f"{node_name} --> {child.name()};")
    if node.without:
        if node.run_last:
            test_edges.append(f"{node.without.name()} -.- {node_name};")
        else:
            teardown_edges.append(f"{node.without.name()} -.- {node_name};")
    return test_edges, teardown_edges


def graph(root=TEST_ROOT):
    visited_nodes = set()
    unvisited_nodes = {root}
    test_edges = []
    teardown_edges = []
    while unvisited_nodes:
        node = unvisited_nodes.pop()
        visited_nodes.add(node)
        unvisited_nodes.update([child for child in node.children if child not in visited_nodes])
        new_test_edges, new_teardown_edges = mermaid_edges(node)
        test_edges.extend(new_test_edges)
        teardown_edges.extend(new_test_edges)
    return (
        "graph TD;\nsubgraph tests\n" + "\n".join(test_edges) +
        "\nsubgraph teardown\n" + "\n".join(teardown_edges)
    )
