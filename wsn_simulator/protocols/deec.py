from config import Config

def run_deec_round(network, round_idx):
    """
    Literature-faithful DEEC (Qing et al., 2006).
    Applies strict heterogeneous constraints where a node's CH probability 
    dynamically scales with the ratio of its residual energy to the network's average.
    Now properly uses per-node RNG tracking securely.
    """
    alive = network.get_alive_nodes()
    if not alive: return
    
    E_avg = network.get_average_energy()
    p_opt = Config.OPTIMAL_CH_PROB
    
    for n in alive:
        n.is_ch = False
        
    for n in alive:
        # DEEC Ratio: p_i = p_opt * (E_i / E_avg)
        p_i = p_opt * (n.energy / E_avg) if E_avg > 0 else 0
        int_pi = max(1, int(1/p_i)) if p_i > 0 else 1
        
        # Epoch gating dynamically scaled by energy
        if (round_idx - n.last_ch_round) >= int_pi:
            denominator = 1 - p_i * (round_idx % int_pi)
            thres = p_i / denominator if (p_i > 0 and denominator > 0) else p_opt
            
            if network.rng.rand() < thres:
                n.is_ch = True
                n.ch_count += 1
                n.last_ch_round = round_idx
