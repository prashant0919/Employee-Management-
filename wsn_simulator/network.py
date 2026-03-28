import numpy as np
from node import Node
from config import Config

class Network:
    def __init__(self, seed):
        self.nodes = []
        self.seed = seed
        self.rng = np.random.RandomState(self.seed)
        
        for i in range(Config.NUM_NODES):
            x = self.rng.uniform(0, Config.AREA_X)
            y = self.rng.uniform(0, Config.AREA_Y)
            e_init = self.rng.uniform(Config.E_INIT_MIN, Config.E_INIT_MAX)
            self.nodes.append(Node(i, x, y, e_init))
            
    def get_alive_nodes(self):
        return [n for n in self.nodes if n.alive]
        
    def get_total_residual_energy(self):
        return sum(n.energy for n in self.get_alive_nodes())
        
    def get_average_energy(self):
        alive = self.get_alive_nodes()
        if not alive: return 0.0
        return sum(n.energy for n in alive) / len(alive)
        
    def reset_nodes(self):
        for n in self.nodes:
            n.reset_round_state()
