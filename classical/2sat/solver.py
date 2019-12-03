from collections import namedtuple, defaultdict

var = namedtuple("var", ["hat", "id"])
not_ = lambda v: var(not v.hat, v.id)


def topological_sort(adj):
    sort = []
    seen = set()

    def dfs(node):
        if node in seen:
            return

        seen.add(node)
        for neighbor in adj[node]:
            dfs(neighbor)

        sort.append(node)

    for node in adj:
        dfs(node)

    sort.reverse()
    return sort


def transpose(adj):
    t_adj = dict()
    for node in adj:
        if node not in t_adj:
            t_adj[node] = set()

        for neighbor in adj[node]:
            if neighbor not in t_adj:
                t_adj[neighbor] = set()

            t_adj[neighbor].add(node)

    return t_adj


def strongly_connected_components(adj, sort):
    t_adj = transpose(adj)
    seen = set()

    def dfs(node, component):
        if node in seen:
            return

        seen.add(node)
        component.add(node)

        for neighbor in t_adj[node]:
            dfs(neighbor, component)

    components = []
    for node in sort:
        if node in seen:
            continue

        component = set()
        dfs(node, component)

        components.append(component)

    return components


def clauses_to_graph(clauses):
    adj = defaultdict(set)

    for (a, b) in clauses:
        adj[a], adj[b]  # create keys
        adj[not_(a)].add(b)
        adj[not_(b)].add(a)

    return dict(adj)


def check_2sat(clauses, values):
    value = lambda c: not values[c.id] if c.hat else values[c.id]
    return all(value(c1) or value(c2) for (c1, c2) in clauses)


def solve_2sat(clauses):
    # convert clauses to graph
    adj = clauses_to_graph(clauses)

    # topologically sort graph
    sort = topological_sort(adj)

    # extract strongly connect components
    components = strongly_connected_components(adj, sort)

    # check that this instance of 2sat is feasible
    for component in components:
        for node in component:
            # if x and not(x) are in the same strongly connected component: impossible
            if not_(node) in component:
                return None

    values = dict()

    # process strongly connected component in reversed topological order
    node_to_component = {
        node: component for component in components for node in component
    }
    for node in reversed(sort):
        # skip strongly connected component is it has already been processed
        if node.id in values:
            continue

        for node in node_to_component[node]:
            values[node.id] = not node.hat

    return values
