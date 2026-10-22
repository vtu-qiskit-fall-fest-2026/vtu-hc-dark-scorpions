"""QAOA solver using MinimumEigenOptimizer."""
import numpy as np
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.applications import MaxCut
from qiskit_optimization.algorithms import MinimumEigenOptimizer
import networkx as nx


def quantum_maxcut(G: nx.Graph, n: int, reps: int = 2) -> tuple:
    """
    Solve MaxCut using QAOA via MinimumEigenOptimizer.

    Args:
        G: NetworkX graph
        n: Number of nodes
        reps: Number of QAOA layers (p)

    Returns:
        (cut_value, partition_array, energy)
    """
    maxcut = MaxCut(G)
    qp = maxcut.to_quadratic_program()

    sampler = StatevectorSampler()
    qaoa = QAOA(sampler, COBYLA(maxiter=200), reps=reps)

    optimizer = MinimumEigenOptimizer(qaoa)
    result = optimizer.solve(qp)

    optimal = result.x.astype(int)
    cut = sum(1 for u, v in G.edges() if optimal[u] != optimal[v])
    return cut, optimal, result.fval   
