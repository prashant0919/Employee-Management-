import numpy as np
from config import Config

class MetricsTracker:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes

        self.round_hist = []
        self.alive_hist = []
        self.dead_hist = []
        self.energy_hist = []
        self.avg_energy_alive_hist = []
        self.energy_var_hist = []
        self.fairness_hist = []
        self.ch_count_hist = []

        self.packets_round_hist = []
        self.packets_bs_cum_hist = []
        self.packets_sent_hist = self.packets_bs_cum_hist

        self.coverage_hist = []

        self.fnd = None
        self.hnd = None
        self.lnd = None

        self.total_packets_to_bs = 0
        self.death_round_by_node = {i: None for i in range(num_nodes)}
        self.ch_selection_count = {i: 0 for i in range(num_nodes)}

    @staticmethod
    def jain_fairness(values):
        arr = np.asarray(values, dtype=float)
        if arr.size == 0:
            return 0.0
        denom = arr.size * np.sum(arr ** 2)
        if denom <= Config.FAIRNESS_EPS:
            return 0.0
        return float((np.sum(arr) ** 2) / denom)

    def log_round(self, round_idx, network, selected_ch_ids, packets_to_bs, coverage_ratio=None):
        nodes = network.nodes
        alive_nodes = [n for n in nodes if n.alive]
        alive_count = len(alive_nodes)

        alive_energies = np.asarray([n.energy for n in alive_nodes], dtype=float)
        total_energy = float(alive_energies.sum()) if alive_energies.size else 0.0
        avg_energy_alive = float(alive_energies.mean()) if alive_energies.size else 0.0
        energy_var_alive = float(alive_energies.var()) if alive_energies.size > 1 else 0.0
        fairness_alive = self.jain_fairness(alive_energies)

        self.round_hist.append(round_idx)
        self.alive_hist.append(alive_count)
        self.dead_hist.append(self.num_nodes - alive_count)
        self.energy_hist.append(total_energy)
        self.avg_energy_alive_hist.append(avg_energy_alive)
        self.energy_var_hist.append(energy_var_alive)
        self.fairness_hist.append(fairness_alive)
        self.ch_count_hist.append(len(selected_ch_ids))

        self.packets_round_hist.append(int(packets_to_bs))
        self.total_packets_to_bs += int(packets_to_bs)
        self.packets_bs_cum_hist.append(self.total_packets_to_bs)

        self.coverage_hist.append(np.nan if coverage_ratio is None else float(coverage_ratio))

        for node_id in selected_ch_ids:
            self.ch_selection_count[node_id] += 1

        for n in nodes:
            if (not n.alive) and self.death_round_by_node[n.id] is None:
                self.death_round_by_node[n.id] = round_idx

        if self.fnd is None and alive_count < self.num_nodes:
            self.fnd = round_idx

        if self.hnd is None and alive_count <= (self.num_nodes / 2):
            self.hnd = round_idx

        if self.lnd is None and alive_count == 0:
            self.lnd = round_idx

    def finalize(self, max_rounds):
        if self.fnd is None:
            self.fnd = max_rounds
        if self.hnd is None:
            self.hnd = max_rounds
        if self.lnd is None:
            self.lnd = max_rounds

        for node_id, death_round in self.death_round_by_node.items():
            if death_round is None:
                self.death_round_by_node[node_id] = max_rounds