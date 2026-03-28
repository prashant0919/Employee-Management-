import math
from config import Config

class Node:
    def __init__(self, node_id, x, y, initial_energy):
        self.id = node_id
        self.x = x
        self.y = y
        self.initial_energy = initial_energy
        self.energy = initial_energy
        self.alive = True

        self.is_ch = False
        self.is_optimal_tier = True
        self.ch_count = 0
        self.last_ch_round = -10**9

        self.dist_to_bs = math.hypot(self.x - Config.BS_X, self.y - Config.BS_Y)

    def consume_energy(self, amount):
        if not self.alive:
            return
        self.energy -= amount
        if self.energy <= 0:
            self.energy = 0.0
            self.alive = False

    def distance_to(self, other_node):
        return math.hypot(self.x - other_node.x, self.y - other_node.y)

    def reset_round_state(self):
        self.is_ch = False