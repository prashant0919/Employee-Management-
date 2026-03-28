import math
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from config import Config

class ProposedState:
    last_variance = None
    last_tier_calc = 0
    optimal_tier_ids = set()

    @classmethod
    def reset(cls):
        cls.last_variance = None
        cls.last_tier_calc = 0
        cls.optimal_tier_ids = set()

def reset_proposed_state():
    ProposedState.reset()

def _build_feature_matrix(alive):
    max_d_bs = max((n.dist_to_bs for n in alive), default=1.0)
    max_energy = max((n.energy for n in alive), default=1.0)

    cx = Config.AREA_X / 2.0
    cy = Config.AREA_Y / 2.0
    max_center_dist = math.hypot(cx, cy) or 1.0

    rows = []
    for n in alive:
        center_dist = math.hypot(n.x - cx, n.y - cy)
        # Formally renamed feature representation from "Centrality" to true parameter definition
        field_center_proximity = 1.0 - (center_dist / max_center_dist)
        sink_proximity = 1.0 - (n.dist_to_bs / max_d_bs)
        rows.append([
            n.energy / max_energy if max_energy > 0 else 0.0,
            field_center_proximity,
            sink_proximity,
        ])
    return np.asarray(rows, dtype=float)

def _recompute_optimal_tier(alive, rng):
    if len(alive) < 4:
        ProposedState.optimal_tier_ids = {n.id for n in alive}
        return

    X = _build_feature_matrix(alive)
    best_score = -np.inf
    best_labels = None

    upper_k = min(5, len(alive) - 1)
    
    seed_int = int(rng.randint(0, 100000))
    for k in range(2, upper_k + 1):
        model = KMeans(n_clusters=k, random_state=seed_int, n_init=10)
        labels = model.fit_predict(X)

        if len(set(labels)) < 2:
            continue

        score = silhouette_score(X, labels)
        if score > best_score:
            best_score = score
            best_labels = labels

    if best_labels is None:
        ProposedState.optimal_tier_ids = {n.id for n in alive}
        return

    best_cluster = None
    best_cluster_strength = -np.inf

    for label in set(best_labels):
        idx = np.where(best_labels == label)[0]
        cluster_X = X[idx]
        strength = 0.7 * cluster_X[:, 0].mean() + 0.3 * cluster_X[:, 2].mean()
        if strength > best_cluster_strength:
            best_cluster_strength = strength
            best_cluster = label

    ProposedState.optimal_tier_ids = {
        alive[i].id for i, label in enumerate(best_labels) if label == best_cluster
    }

def run_proposed_round(network, round_idx):
    """
    Custom Method: Energy-Variance-Triggered Adaptive K-Means Capability Tiering.
    Combines strict energy constraints with completely unsupervised physical tiering logic.
    Renamed 'centrality' to 'field_center_proximity' for literature fidelity and fairness.
    """
    alive = network.get_alive_nodes()
    if not alive:
        return

    for n in alive:
        n.is_ch = False

    num_ch = max(1, int(round(len(alive) * Config.OPTIMAL_CH_PROB)))

    energies = np.asarray([n.energy for n in alive], dtype=float)
    curr_var = float(energies.var()) if energies.size > 1 else 0.0
    mean_energy = float(energies.mean()) if energies.size else 0.0

    alive_ids = {n.id for n in alive}
    cached_ids_stale = len(ProposedState.optimal_tier_ids - alive_ids) > 0

    refresh = (
        ProposedState.last_variance is None
        or abs(curr_var - ProposedState.last_variance) > (0.02 * max(mean_energy, 1e-12))
        or (round_idx - ProposedState.last_tier_calc) >= 25
        or cached_ids_stale
    )

    if refresh:
        ProposedState.last_variance = curr_var
        ProposedState.last_tier_calc = round_idx
        _recompute_optimal_tier(alive, network.rng)

    for n in alive:
        n.is_optimal_tier = (n.id in ProposedState.optimal_tier_ids)

    opt_pool = [n for n in alive if n.is_optimal_tier]
    if len(opt_pool) < num_ch:
        opt_pool = alive

    avg_e = np.mean([n.energy for n in opt_pool]) if opt_pool else 1.0
    if avg_e <= 0:
        avg_e = 1.0

    scored = []
    for n in opt_pool:
        energy_term = n.energy / avg_e
        fairness_term = 1.0 / (1.0 + 0.5 * n.ch_count)
        score = (energy_term * fairness_term) * (0.7 + 0.6 * network.rng.rand())
        scored.append((score, network.rng.rand(), n))

    scored.sort(reverse=True)

    for _, _, node in scored[:num_ch]:
        node.is_ch = True
        node.ch_count += 1
        node.last_ch_round = round_idx

run_proposed_round.reset_state = reset_proposed_state