import math

class Config:
    AREA_X = 100
    AREA_Y = 100
    BS_X = 50
    BS_Y = 150

    NUM_NODES = 100
    E_INIT_MIN = 0.50
    E_INIT_MAX = 0.50

    # First-order radio model
    E_ELEC = 50e-9
    E_FS = 10e-12
    E_MP = 0.0013e-12
    E_DA = 5e-9
    D0 = math.sqrt(E_FS / E_MP)

    PACKET_SIZE = 4000
    MAX_ROUNDS = 2000
    OPTIMAL_CH_PROB = 0.05

    SENSING_ENERGY_PER_ROUND = PACKET_SIZE * E_ELEC
    FAIRNESS_EPS = 1e-12
    CI_Z = 1.96

    RESULTS_DIR = "results"