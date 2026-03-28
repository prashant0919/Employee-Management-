# Required Decision Phase: WSN Cluster Head Selection Simulation

## 1. Selected Adaptive Unsupervised Method
**Energy-Variance-Triggered Adaptive K-Means Capability Tiering**.  
Instead of performing costly geographic clustering every round, the Base Station (BS) triggers K-Means clustering only when the network's global energy variance shifts beyond a threshold. It clusters nodes into abstract "Capability Tiers" based on three features: Normalized Residual Energy, Node Centrality (reciprocal of sum of distances to neighbors), and Distance to Sink. The optimal number of tiers ($K$) is dynamically selected using the Silhouette Score. 

## 2. Why it fits the title
The title is "Dynamic Cluster Head Selection in Wireless Sensor Networks Using Adaptive Unsupervised Learning". 
- **Unsupervised Learning:** Standard K-Means.
- **Adaptive:** Adapts structurally (finds optimal $K$ naturally instead of a hardcoded value) and temporally (triggers only when energy instability is detected, rather than wastefully every round).
- **Dynamic Cluster Head Selection:** Rotates CHs dynamically among the discovered "Optimal Tier", preventing weak nodes from dying prematurely.

## 3. Selected Baselines
1. **LEACH (Low-Energy Adaptive Clustering Hierarchy)**
2. **HEED (Hybrid Energy-Efficient Distributed clustering)**
3. **DEEC (Distributed Energy-Efficient Clustering)**

## 4. Why these baselines are the right comparison set
- **LEACH** defines the core stochastic benchmark. No energy-awareness; random CH rotation.
- **DEEC** is the definitive benchmark for heterogeneous networks, using global average energy to adjust strict probability metrics.
- **HEED** represents iterative, cost-based CH selection combining energy and communication cost (node degree/distance), serving as the primary deterministic benchmark. 
Comparing the proposed AI method against the purely stochastic (LEACH), the probabilistically-adjusted (DEEC), and the topologically-aware (HEED) algorithms demonstrates unassailable rigor.

## 5. Homogeneous vs. Heterogeneous Setup
The simulation will assume a **Heterogeneous** energy environment. Nodes will be initialized with small uniform variance in their initial energy (e.g., $E_{init} \in [0.4, 0.6] J$). 
*Why:* DEEC is specifically formulated to prove its superiority in heterogeneous settings. Running DEEC and HEED against the proposed method in a strictly homogeneous network weakens the evaluation. Real-world IoT deployments display energy heterogeneity rapidly due to environmental factors. Providing baseline heterogeneity makes the simulation publication-grade.

## 6. Literature Ambiguity & Implementation Choices
**HEED implementation ambiguity:** HEED's original paper relies on intra-round iterative message passing $CH_{prob} = C_{prob} \times \frac{E_{residual}}{E_{max}}$ strictly to finalize clusters without a central BS. In round-based macro-simulations, simulating thousands of micro-messages per round introduces O(N^2) complexity not captured by standard simulators. 
*Approximation:* We implement HEED's core mathematical CH eligibility probability directly at the simulation engine level per round, simulating the cost-based tie-breaking for non-CH nodes instantly by calculating intra-cluster distances. This preserves HEED's mathematical intent for energy consumption and CH distribution while being cleanly executable.
