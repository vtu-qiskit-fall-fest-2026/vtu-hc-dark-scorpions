"""QAOA circuit construction for MaxCut."""
from qiskit import QuantumCircuit
import networkx as nx


def build_qaoa_circuit(n_qubits: int, edges: list, gammas: list, betas: list) -> QuantumCircuit:
    """
    Build a QAOA circuit for MaxCut.

    Args:
        n_qubits: Number of qubits (= graph nodes)
        edges: List of (u, v) tuples
        gammas: Cost layer angles (length = p)
        betas:  Mixer layer angles (length = p)

    Returns:
        QuantumCircuit
    """
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))

    for gamma, beta in zip(gammas, betas):
        # Cost layer: for each edge (u, v), apply CX-RZ-CX
        for u, v in edges:
            qc.cx(u, v)
            qc.rz(2 * gamma, v)
            qc.cx(u, v)
        # Mixer layer: RX on all qubits
        for q in range(n_qubits):
            qc.rx(2 * beta, q)

    return qc


def get_edges(G: nx.Graph) -> list:
    """Extract edge list from a NetworkX graph."""
    return list(G.edges())   
