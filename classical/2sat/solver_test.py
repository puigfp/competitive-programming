from solver import (
    var,
    topological_sort,
    transpose,
    strongly_connected_components,
    clauses_to_graph,
    check_2sat,
    solve_2sat,
)


def test_topological_sort():
    assert topological_sort(dict()) == []

    adj = {1: {2, 3}, 2: {}, 3: {2}}
    assert topological_sort(adj) == [1, 3, 2]

    adj = {1: {3}, 2: {1}, 3: {2}}
    assert topological_sort(adj) == [1, 3, 2]


def test_transpose():
    assert transpose(dict()) == dict()

    adj = {1: {2, 3}, 2: set(), 3: {2}}
    assert transpose(adj) == {1: set(), 2: {1, 3}, 3: {1}}


def test_strongly_connected_components():
    assert strongly_connected_components(dict(), topological_sort(dict())) == []

    adj = {1: {2, 3}, 2: {}, 3: {2}}
    assert strongly_connected_components(adj, topological_sort(adj)) == [{1}, {3}, {2}]

    adj = {1: {3}, 2: {1}, 3: {2}}
    assert strongly_connected_components(adj, topological_sort(adj)) == [{1, 2, 3}]

    adj = {1: {2, 3}, 2: {1, 4}, 3: {4}, 4: {3}}
    assert strongly_connected_components(adj, topological_sort(adj)) == [{1, 2}, {3, 4}]


def test_clauses_to_graph():
    assert clauses_to_graph([]) == dict()

    clauses = [
        (var(True, 1), var(True, 2)),
        (var(True, 2), var(True, 3)),
        (var(False, 1), var(False, 3)),
    ]
    assert clauses_to_graph(clauses) == {
        var(True, 1): {var(False, 3)},
        var(True, 2): set(),
        var(True, 3): {var(False, 1)},
        var(False, 1): {var(True, 2)},
        var(False, 2): {var(True, 1), var(True, 3)},
        var(False, 3): {var(True, 2)},
    }


def test_solve_2sat():
    assert solve_2sat([]) == dict()

    # impossible case
    clauses = [
        (var(False, 1), var(False, 2)),
        (var(False, 1), var(True, 2)),
        (var(True, 1), var(False, 2)),
        (var(True, 1), var(True, 2)),
    ]
    assert solve_2sat(clauses) is None

    clauses = [
        (var(False, 1), var(False, 2)),
        (var(False, 2), var(False, 3)),
        (var(True, 1), var(True, 3)),
    ]
    assert check_2sat(clauses, solve_2sat(clauses))

    clauses = [
        # 1, 2 and 3 should have the same value
        (var(True, 1), var(False, 2)),
        (var(True, 2), var(False, 3)),
        (var(True, 3), var(False, 1)),

        # 4 and 5 should have the same value
        (var(True, 4), var(False, 5)),
        (var(True, 5), var(False, 4)),

        # 6 and 7 should have the same value
        (var(True, 6), var(False, 7)),
        (var(True, 7), var(False, 6)),

        # create some links between components
        (var(False, 1), var(False, 4)),
        (var(False, 1), var(False, 7)),
    ]
    assert check_2sat(clauses, solve_2sat(clauses))
