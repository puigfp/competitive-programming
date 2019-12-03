from solve import is_above, topological_sort, init_segment_tree, query, add_update

def test_is_above():
    assert True == is_above(((3, 8), (7, 7)), ((5, 5), (9, 3)))
    assert False == is_above(((1, 7), (5, 6)), ((3, 8), (7, 7)))


def test_topological_sort():
    adj = [[], [2, 3, 4, 0], [4], [2, 4], [0], []]
    assert [1, 5, 3, 2, 4, 0] == topological_sort(adj)


def test_segment_tree():
    tree = init_segment_tree([1] * 6)
    assert 3 == query(0, 3, tree)
    assert 6 == query(0, 8, tree)
    assert 0 == query(6, 8, tree)

    add_update(0, 6, 2, tree)
    assert 6 == query(0, 3, tree)
    assert 12 == query(0, 8, tree)

    add_update(0, 8, 0, tree)
    add_update(0, 2, 10, tree)
    add_update(4, 6, -12, tree)
    add_update(0, 6, 1, tree)
    add_update(0, 1, 3, tree)
    add_update(2, 6, -1, tree)
    assert 3 == query(0, 3, tree)
    assert 0 == query(0, 6, tree)
    assert 1 == query(1, 2, tree)
