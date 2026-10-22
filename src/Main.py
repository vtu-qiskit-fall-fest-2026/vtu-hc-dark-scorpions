"""
Orchestrator: CLI test without Streamlit.
Run: python -m src.main
"""
import networkx as nx
import numpy as np
import time
from src.classical import classical_maxcut
from src.optimizer import quantum_maxcut


def run_comparison(n_nodes: int = 4, reps: int = 2, seed: int = 42):
    np.random.seed(seed)
    G = nx.gnp_graph(n_nodes, 0.6, seed=seed)

    print(f"\n{'='*50}")
    print(f"  Graph: {n_nodes} nodes, {G.number_of_edges()} edges")
    print(f"{'='*50}")

    t0 = time.time()
    c_cut, c_part = classical_maxcut(G, n_nodes)
    c_time = time.time() - t0
    print(f"\n🖥️  Classical (Brute Force)")
    print(f"   Cut: {c_cut} | Time: {c_time*1000:.2f} ms | Partition: {c_part}")

    t0 = time.time()
    q_cut, q_part, q_energy = quantum_maxcut(G, n_nodes, reps)
    q_time = time.time() - t0
    print(f"\n⚛️  Quantum (QAOA, p={reps})")
    print(f"   Cut: {q_cut} | Time: {q_time*1000:.2f} ms | Partition: {list(q_part)}")
    print(f"   Energy: {q_energy:.4f}")

    print(f"\n{'='*50}")
    if q_cut == c_cut:
        print(f"  ✅ QAOA found optimal solution (cut = {c_cut})")
    else:
        print(f"  ⚠️  QAOA: {q_cut}/{c_cut} (ratio: {q_cut/c_cut:.2%})")
    print(f"{'='*50}\n")

    return c_cut, q_cut


if __name__ == "__main__":
    run_comparison(n_nodes=4, reps=2)   
