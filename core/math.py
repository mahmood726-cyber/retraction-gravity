import numpy as np

def propagate_retraction_gravity(nodes, edges, retraction_event_node_id, gravity_attenuation=0.8):
    """
    Propagates a reliability shock through a Directed Acyclic Graph (DAG).
    Simulates how a retracted trial or flawed method affects dependent projects.
    """
    # Initialize reliability scores
    reliability = {n['id']: 1.0 for n in nodes} # Assume perfect initial TruthCert
    
    # Apply the primary shock (Retraction = 0.0 reliability)
    if retraction_event_node_id in reliability:
        reliability[retraction_event_node_id] = 0.0
        
    # Build adjacency list (Parent -> Children)
    adj = {n['id']: [] for n in nodes}
    for e in edges:
        adj[e['source']].append(e['target'])
        
    # BFS to propagate gravity
    # In a real DAG, we'd do topological sort to handle multiple parents correctly
    queue = [retraction_event_node_id]
    visited = set()
    
    while queue:
        current = queue.pop(0)
        if current in visited: continue
        visited.add(current)
        
        current_rel = reliability[current]
        
        for child in adj[current]:
            # The child's reliability drops based on the parent's failure + attenuation
            # E.g., if parent is 0.0, child becomes 0.2 (if attenuation is 0.8)
            # If a child has multiple paths, it takes the worst (minimum) reliability
            shock = current_rel + (1.0 - current_rel) * (1.0 - gravity_attenuation)
            reliability[child] = min(reliability[child], shock)
            
            queue.append(child)
            
    return reliability

def calculate_portfolio_health(reliability_scores):
    """
    Computes the overall health of the portfolio.
    """
    scores = list(reliability_scores.values())
    if not scores: return 0.0
    return float(np.mean(scores) * 100)
