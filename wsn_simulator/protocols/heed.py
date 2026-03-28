from config import Config

def run_heed_round(network, round_idx):
    """
    Simplified Iterative HEED (Younis & Fahmy, 2004).
    Approximates iterative convergence within a discrete simulation round dynamically.
    Preserves HEED's dual mechanics: primary probability driven by residual energy,
    and iterative probability doubling until full spatial coverage is achieved.
    """
    alive = network.get_alive_nodes()
    if not alive: return
    
    for n in alive:
        n.is_ch = False
        
    E_max = Config.E_INIT_MAX
    C_prob = Config.OPTIMAL_CH_PROB
    
    final_chs = []
    uncovered = set(alive)
    
    # Phase 1: Initialize probability exact to HEED
    ch_probs = {}
    for n in alive:
        base_prob = C_prob * (n.energy / E_max) if E_max > 0 else 0
        ch_probs[n] = max(C_prob * 0.01, min(1.0, base_prob))
        
    Rs = min(Config.AREA_X, Config.AREA_Y) * 0.35 # Standard spatial coverage heuristic radius
    max_iterations = 6 # Typical upper bound for HEED probability doubling mechanics
    
    # Phase 2: Iterative probability simulation logic
    for step in range(max_iterations):
        if not uncovered: break
        
        step_chs = []
        for n in list(uncovered):
            if network.rng.rand() < ch_probs[n]:
                step_chs.append(n)
                
        # Phase 3: Coverage and secondary cost assignment (approximating AMF)
        for ch in step_chs:
            if ch not in final_chs:
                final_chs.append(ch)
                ch.is_ch = True
                ch.ch_count += 1
                ch.last_ch_round = round_idx
                
            coverage_targets = [nc for nc in list(uncovered) if nc.distance_to(ch) <= Rs]
            for c_node in coverage_targets:
                uncovered.discard(c_node)
                
        # Iteration doubling for nodes that securely failed to locate coverage
        for n in list(uncovered):
            ch_probs[n] = min(1.0, ch_probs[n] * 2.0)
            if ch_probs[n] == 1.0:
                final_chs.append(n)
                n.is_ch = True
                n.ch_count += 1
                n.last_ch_round = round_idx
                uncovered.discard(n)
                
                # Cleanup sweep
                sweep_targets = [nc for nc in list(uncovered) if nc.distance_to(n) <= Rs]
                for c_node in sweep_targets:
                    uncovered.discard(c_node)
