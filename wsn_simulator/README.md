# WSN Simulator for Dynamic Cluster Head Selection

This repository contains a reproducible, research-grade Python simulation for evaluating the "Dynamic Cluster Head Selection in Wireless Sensor Networks Using Adaptive Unsupervised Learning" mechanism against standard WSN clustering baselines (LEACH, DEEC, HEED).

## Directory Structure
- `config.py`: Simulation parameters, first-order radio constants, energy states.
- `energy_model.py`: Transmitter, receiver, and aggregation energy mechanics.
- `node.py`, `network.py`: Physical representations of WSN sensors and the grid.
- `protocols/`: Contains algorithms for CH execution:
  - `leach.py`: Pure stochastic.
  - `deec.py`: Deterministic heterogeneity tracker.
  - `heed.py`: Energy and Cost approximation.
  - `proposed.py`: Energy-Variance-Triggered Adaptive K-Means.
- `simulator.py`, `metrics.py`: The core engine driving round logic and metric capturing.
- `experiments.py`, `plotting.py`: Monte Carlo orchestrator and result generators.

## How to Run
```bash
pip install -r requirements.txt
python3 main.py --runs 5
```

## Expected Outputs
Running the simulation will output a comprehensive `summary_results.csv` logging the exact FND, HND, and LND values across Monte Carlo runs, alongside mean and std. It exports `alive_nodes_plot.png` and `packets_plot.png` demonstrating statistical advantages.
