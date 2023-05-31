from io import StringIO
from typing import List

from entest.const import STATUS
from entest.dependency_decorator import TEST_ROOT, TestCase


def mermaid_edges(node: TestCase):
    node_name = node.name()
    test_edges = []
    teardown_edges = []
    for child in node.children:
        if child.run_last:
            teardown_edges.append(f"{node_name} --> {child.name()}")
        else:
            test_edges.append(f"{node_name} --> {child.name()}")
    if node.without:
        if node.run_last:
            teardown_edges.append(f"{node.without.name()} -.- {node_name}")
        else:
            test_edges.append(f"{node.without.name()} -.- {node_name}")
    return test_edges, teardown_edges


output = StringIO()


def printer(s, prefix="  "):
    print(prefix, s, file=output)


def graph(root=TEST_ROOT):
    eligible_tests = filter_nodes(root.children)
    if len(eligible_tests) == 0:
        return ""
    unvisited_nodes = set(eligible_tests)
    test_edges = []
    teardown_edges = []
    visited_nodes = {root}
    while unvisited_nodes:
        node = unvisited_nodes.pop()
        visited_nodes.add(node)
        unvisited_nodes.update([child for child in node.children if child not in visited_nodes])
        new_test_edges, new_teardown_edges = mermaid_edges(node)
        test_edges.extend(new_test_edges)
        teardown_edges.extend(new_teardown_edges)
    printer("flowchart TD", prefix="")
    printer("subgraph tests")
    for edge in test_edges:
        printer(edge)
    printer("end")
    if len(teardown_edges) > 0:
        printer("subgraph teardown")
        for edge in teardown_edges:
            printer(edge)
        printer("end")
    return output.getvalue()


def filter_nodes(nodes: List["TestCase"]):
    return [node for node in nodes if node.status != STATUS.none]
