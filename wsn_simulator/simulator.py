from network import Network
from metrics import MetricsTracker
from energy_model import transmit_energy, receive_energy, aggregate_energy, sensing_energy
from config import Config

class WSN_Simulator:
    def __init__(self, seed, protocol_func):
        self.network = Network(seed)
        self.protocol_func = protocol_func
        self.metrics = MetricsTracker(Config.NUM_NODES)

    def run(self):
        for round_idx in range(1, Config.MAX_ROUNDS + 1):
            self.network.reset_nodes()

            alive = self.network.get_alive_nodes()
            if not alive:
                break

            self._apply_sensing_cost()

            alive = self.network.get_alive_nodes()
            if not alive:
                self.metrics.log_round(round_idx, self.network, [], 0)
                break

            self.protocol_func(self.network, round_idx)

            selected_ch_ids = [n.id for n in self.network.get_alive_nodes() if n.is_ch]
            packets_to_bs = self._execute_communication_phase()

            self.metrics.log_round(
                round_idx=round_idx,
                network=self.network,
                selected_ch_ids=selected_ch_ids,
                packets_to_bs=packets_to_bs,
                coverage_ratio=None,
            )

        self.metrics.finalize(Config.MAX_ROUNDS)
        return self.metrics

    def _apply_sensing_cost(self):
        for node in self.network.get_alive_nodes():
            self._consume_if_possible(node, sensing_energy())

    def _consume_if_possible(self, node, amount):
        if not node.alive:
            return False

        success = node.energy + 1e-15 >= amount
        node.consume_energy(amount)
        return success

    def _execute_communication_phase(self):
        packets_to_bs = 0

        alive = self.network.get_alive_nodes()
        selected_chs = [n for n in alive if n.is_ch]

        if not selected_chs:
            for node in list(alive):
                tx_cost = transmit_energy(node.dist_to_bs)
                if self._consume_if_possible(node, tx_cost):
                    packets_to_bs += 1
            return packets_to_bs

        clusters = {ch.id: [] for ch in selected_chs}

        for node in list(alive):
            if node.is_ch:
                continue

            nearest_ch = min(selected_chs, key=lambda ch: node.distance_to(ch))
            tx_cost = transmit_energy(node.distance_to(nearest_ch))

            sent_ok = self._consume_if_possible(node, tx_cost)
            if sent_ok:
                clusters[nearest_ch.id].append(node.id)

        for ch in selected_chs:
            if not ch.alive:
                continue

            member_count = len(clusters[ch.id])

            rx_ok = self._consume_if_possible(ch, receive_energy() * member_count)
            if not rx_ok:
                continue

            aggr_ok = self._consume_if_possible(ch, aggregate_energy(member_count + 1))
            if not aggr_ok:
                continue

            tx_ok = self._consume_if_possible(ch, transmit_energy(ch.dist_to_bs))
            if tx_ok:
                packets_to_bs += 1

        return packets_to_bs