"""Brute-force classical MaxCut solver."""
import networkx as nx


def classical_maxcut(G: nx.Graph, n: int) -> tuple:
    """
    Solve MaxCut by exhaustive search over all 2^n partitions.

    Args:
        G: NetworkX graph
        n: Number of nodes

    Returns:
        (best_cut_value, best_partition_tuple)
    """
    best_cut = 0
    best_partition = None

    for mask in range(2 ** n):
        partition = tuple((mask >> i) & 1 for i in range(n))
        cut = sum(1 for u, v in G.edges() if partition[u] != partition[v])
        if cut > best_cut:
            best_cut = cut
            best_partition = partition

    return best_cut, best_partition   
