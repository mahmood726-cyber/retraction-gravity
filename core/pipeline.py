import datetime
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(REPO_ROOT)

from core.math import calculate_portfolio_health, propagate_retraction_gravity

RESULTS_PATH = os.path.join(REPO_ROOT, "data", "gravity_results.json")

def run_pipeline(output_path=None):
    # Simulated Portfolio Graph (Nodes = Projects/Datasets, Edges = Dependencies)
    nodes = [
        {"id": "DATA_GBD2023", "label": "GBD 2023 Covariates", "type": "dataset"},
        {"id": "DATA_TrialX", "label": "Clinical Trial X (Cardio)", "type": "dataset"},
        {"id": "METH_SmithLogit", "label": "Smith-Logit Transform", "type": "method"},
        {"id": "PROJ_Transport", "label": "Global Transportability Atlas", "type": "project"},
        {"id": "PROJ_ProgMeta", "label": "Prognostic-Meta (PROBAST)", "type": "project"},
        {"id": "PROJ_CardioRisk", "label": "Cardio Risk Dashboard", "type": "project"},
        {"id": "PROJ_DiabetesRWE", "label": "Diabetes RWE Simulator", "type": "project"}
    ]

    edges = [
        {"source": "DATA_GBD2023", "target": "PROJ_Transport"},
        {"source": "DATA_TrialX", "target": "PROJ_ProgMeta"},
        {"source": "METH_SmithLogit", "target": "PROJ_ProgMeta"},
        {"source": "PROJ_ProgMeta", "target": "PROJ_CardioRisk"},
        {"source": "DATA_GBD2023", "target": "PROJ_DiabetesRWE"},
        {"source": "METH_SmithLogit", "target": "PROJ_DiabetesRWE"}
    ]

    # Scenario 1: Baseline (No Retractions)
    baseline_rel = {n['id']: 1.0 for n in nodes}
    baseline_health = calculate_portfolio_health(baseline_rel)

    # Scenario 2: Trial X is Retracted (Data Fraud)
    # Affects ProgMeta directly, and CardioRisk indirectly
    shock_trial_rel = propagate_retraction_gravity(nodes, edges, "DATA_TrialX", gravity_attenuation=0.5)
    shock_trial_health = calculate_portfolio_health(shock_trial_rel)

    # Scenario 3: Smith-Logit Method is proven mathematically flawed
    # Affects ProgMeta, CardioRisk, and DiabetesRWE
    shock_meth_rel = propagate_retraction_gravity(nodes, edges, "METH_SmithLogit", gravity_attenuation=0.3) # Methods have heavier gravity (less attenuation)
    shock_meth_health = calculate_portfolio_health(shock_meth_rel)

    output = {
        "audit": {
            "methodology": "E156 Retraction Gravity (DAG Shock Propagation)",
            "timestamp": datetime.datetime.now().isoformat()
        },
        "graph": {
            "nodes": nodes,
            "edges": edges
        },
        "scenarios": [
            {
                "id": "baseline",
                "name": "Baseline (All Valid)",
                "portfolio_health": baseline_health,
                "node_reliabilities": baseline_rel
            },
            {
                "id": "shock_trial",
                "name": "Shock: Trial X Retracted",
                "portfolio_health": shock_trial_health,
                "node_reliabilities": shock_trial_rel
            },
            {
                "id": "shock_method",
                "name": "Shock: Smith-Logit Flawed",
                "portfolio_health": shock_meth_health,
                "node_reliabilities": shock_meth_rel
            }
        ]
    }

    target_path = output_path or RESULTS_PATH
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    print("Retraction Gravity pipeline complete. Impact graphs generated.")
    return output

if __name__ == "__main__":
    run_pipeline()
