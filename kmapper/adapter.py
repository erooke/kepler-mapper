""" Adapt Mapper format into other common formats.

    - networkx

"""


def to_networkx(graph):
    """Convert a Mapper 1-complex to a networkx graph.

    Parameters
    -----------

    graph: dictionary, graph object returned from `kmapper.map`

    Returns
    --------

    g: graph as networkx.Graph() object

    """

    # import here so networkx is not always required.
    import networkx as nx

    simplices = graph["simplices"]

    nodes = simplices[0] if len(simplices) >= 1 else list()
    edges = simplices[1] if len(simplices) >= 2 else list()

    g = nx.Graph()
    g.add_nodes_from(nodes)
    nx.set_node_attributes(g, dict(graph["nodes"]), "membership")

    g.add_edges_from(edges)

    return g


to_nx = to_networkx
