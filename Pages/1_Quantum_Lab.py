import streamlit as st
import networkx as nx
import numpy as np
import time
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.applications import Maxcut
from qiskit_optimization.algorithms import MinimumEigenOptimizer
import matplotlib.pyplot as plt

st.set_page_config(page_title="Quantum Optimisation Lab", layout="wide")
st.title("⚛️ Quantum vs Classical: Network Optimisation Lab")
st.caption("Solve real-world optimisation problems using QAOA on the Qiskit Aer simulator")

# ─── SCENARIO SELECTOR ───
st.subheader("🏭 Choose a Real-World Scenario")

scenario = st.selectbox("Application domain", [
    "🔬 VLSI Circuit Partitioning",
    "👥 Social Network Community Detection",
    "🏢 Data Center Rack Partitioning",
    "🚚 Logistics Fleet Scheduling",
    "📊 Financial Portfolio Split",
])

n_nodes = st.slider("Number of nodes (entities)", 3, 6, 4)

# ─── GRAPH GENERATION PER SCENARIO ───
def build_graph(scenario, n):
    """Each scenario generates a different graph structure."""
    if scenario.startswith("🔬"):
        # VLSI: random dense graph (circuits are dense)
        G = nx.gnr_graph(n, 0.7)
        st.info(f"🔬 *Circuit Partitioning:* {n} logic gates, {G.number_of_edges()} wires. "
                f"Goal: split into 2 chips with minimum inter-chip wires.")
    elif scenario.startswith("👥"):
        # Social: two dense clusters + few cross-links
        G = nx.disjoint_union(nx.complete_graph(2), nx.complete_graph(2))
        if n > 4:
            G = nx.gnp_graph(n, 0.4)
            # Add a few cross-community edges
            for i in range(n//2):
                for j in range(n//2, n):
                    if np.random.random() < 0.3:
                        G.add_edge(i, j)
        st.info(f"👥 *Community Detection:* {n} people, {G.number_of_edges()} friendships. "
                f"Goal: find the natural 2-group split (communities).")
    elif scenario.startswith("🏢"):
        # Data center: ring + a few chords
        G = nx.cycle_graph(n)
        G.add_edge(0, n-2)
        if n > 4:
            G.add_edge(1, n-1)
        st.info(f"🏢 *Rack Partitioning:* {n} servers in a ring topology. "
                f"Goal: split into 2 racks with minimum cross-rack traffic.")
    elif scenario.startswith("🚚"):
        # Logistics: complete graph (every location connected)
        G = nx.complete_graph(n)
        st.info(f"🚚 *Fleet Scheduling:* {n} delivery locations. "
                f"Goal: split into 2 truck routes to maximize efficiency.")
    elif scenario.startswith("📊"):
        # Finance: random weighted graph
        G = nx.gnp_graph(n, 0.6)
        st.info(f"📊 *Portfolio Split:* {n} assets. "
                f"Goal: split into 'buy' vs 'sell' to maximize return.")
    return G

G = build_graph(scenario, n_nodes)

# ─── VISUALIZE THE GRAPH ───
G = nx.complete_graph(n_nodes)
pos = nx.spring_layout(G, seed=42)

fig, ax = plt.subplots(1, 1, figsize=(6, 5))
nx.draw(G, pos, ax, with_labels=True,
        node_color='#4a90d9', node_size=600,
        font_color='white', font_weight='bold',
        edge_color='#ccc', width=2)
ax.set_title(f"Complete Graph K_{n_nodes}", fontsize=13, fontweight='bold')
ax.axis('off')

st.pyplot(fig, use_container_width=True)
plt.close()

# ─── SOLVERS ───
reps = st.slider("QAOA layers (p)", 1, 3, 2)

def classical_maxcut(G, n):
    best_cut, best_partition = 0, None
    for mask in range(2**n):
        partition = tuple((mask >> i) & 1 for i in range(n))
        cut = sum(1 for u, v in G.edges() if partition[u] != partition[v])
        if cut > best_cut:
            best_cut, best_partition = cut, partition
    return best_cut, best_partition

def quantum_maxcut(G, n, reps):
    maxcut = Maxcut(G)
    qp = maxcut.to_quadratic_program()

    sampler = StatevectorSampler()
    qaoa = QAOA(sampler, COBYLA(maxiter=200), reps=reps)
    
    # Using MinimumEigenOptimizer to seamlessly parse bits and energy outputs
    optimizer = MinimumEigenOptimizer(qaoa)
    result = optimizer.solve(qp)

    optimal = result.x.astype(int)
    cut = sum(1 for u, v in G.edges() if optimal[u] != optimal[v])
    return cut, optimal, result.fval

# ─── RUN BOTH ───
if st.button("⚡ Solve"):
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🖥️ Classical (Brute Force)")
        t0 = time.time()
        c_cut, c_part = classical_maxcut(G, n_nodes)
        c_time = time.time() - t0
        st.metric("Max Cut Value", c_cut)
        st.write(f"⏱️ Time: {c_time*1000:.2f} ms")
        st.write(f"Partition: {c_part}")
        st.write(f"Search space: 2^{n_nodes} = {2**n_nodes} possibilities")

    with col2:
        st.markdown("#### ⚛️ Quantum (QAOA, p=" + str(reps) + ")")
        t0 = time.time()
        q_cut, q_part, q_energy = quantum_maxcut(G, n_nodes, reps)
        q_time = time.time() - t0
        st.metric("Max Cut Value", q_cut)
        st.write(f"⏱️ Time: {q_time*1000:.2f} ms")
        st.write(f"Partition: {list(q_part)}")
        st.write(f"Optimal Value (Energy): {q_energy:.4f}")

    # ─── COMPARISON ───
    st.markdown("---")
    st.subheader("📊 Comparison")

    # Side-by-side table
    st.table({
        "Metric": ["Cut Value", "Time (ms)", "Method", "Correct?"],
        "Classical": [c_cut, f"{c_time*1000:.2f}", "Brute Force (2ⁿ)", "✅ Exact"],
        "Quantum (QAOA)": [q_cut, f"{q_time*1000:.2f}", f"QAOA p={reps}",
                           "✅ Optimal" if q_cut == c_cut else f"⚠️ {q_cut}/{c_cut}"]
    })

    # Bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(['Classical', 'Quantum (QAOA)'], [c_cut, q_cut],
           color=['#2196F3', '#FF5722'], width=0.5)
    ax.set_ylabel("Cut Value (edges cut)")
    ax.set_title("MaxCut: Classical vs Quantum")
    ax.set_ylim(0, max(c_cut, q_cut) + 1)
    for i, v in enumerate([c_cut, q_cut]):
        ax.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
    st.pyplot(fig)
    plt.close()

    # Verdict
    if q_cut == c_cut:
        st.success(f"✅ QAOA found the *optimal* solution (cut = {c_cut}). "
                   f"Both methods agree. For this problem size, QAOA is competitive.")
    else:
        st.warning(f"⚠️ QAOA found cut = {q_cut}, optimal is {c_cut}. "
                   f"Approximation ratio: {q_cut/c_cut:.2%}. "
                   f"Increase QAOA layers (p) to improve.")

# ─── REAL-WORLD CONTEXT (always visible) ───
st.markdown("---")
st.subheader("🌍 Why This Matters")
st.markdown("""

| Industry | Problem | How MaxCut Helps |
|---|---|---|
| *Semiconductor* | Split a chip into 2 sub-chips | Minimize inter-chip wires (cost + speed) |
| *Social Media* | Detect communities in a graph | Find natural groups for targeted ads / recommendations |
| *Cloud Computing* | Partition servers into racks | Minimize cross-rack network traffic (latency) |
| *Logistics* | Split delivery routes between trucks | Maximize route efficiency |
| *Finance* | Split portfolio into buy/sell | Maximize expected return |

*The key insight:* All of these are NP-hard. Classical brute force scales as 2ⁿ — infeasible past ~30 nodes.
QAOA runs in *polynomial time* (scales with circuit depth, not 2ⁿ), making it viable for larger problems
on future quantum hardware.
""")
