from config import Config

def run_leach_round(network, round_idx):
    """
    Literature-faithful LEACH (Heinzelman et al., 2000).
    Corrects the epoch exclusion logic to use proper history tracking.
    Nodes are excluded from the eligible set G if they were CHs in the current epoch limit.
    """
    alive = network.get_alive_nodes()
    if not alive: return
    p = Config.OPTIMAL_CH_PROB
    for n in alive:
        n.is_ch = False
        
    int_p = max(1, int(1/p)) if p > 0 else 1
    
    # Proper Epoch-style exclusion: Node is eligible if its last CH rotation was outside the current epoch window
    G = [n for n in alive if (round_idx - n.last_ch_round) >= int_p]
    if not G: 
        G = alive # Reset epoch if all nodes were CHs
    
    thres = p / (1 - p * (round_idx % int_p)) if p > 0 else p
    for n in G:
        if network.rng.rand() < thres:
            n.is_ch = True
            n.ch_count += 1
            n.last_ch_round = round_idx
