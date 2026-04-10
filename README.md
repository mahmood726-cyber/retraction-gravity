# Retraction Gravity

A Graph Theory and Bayesian Belief Network engine for mapping the impact of scientific retractions across a portfolio of medical research.

This project treats evidence as an interconnected Directed Acyclic Graph (DAG). If a dataset is retracted or a method is proven flawed, the "gravity" of that failure propagates to all dependent projects, dynamically updating their reliability scores.

## Features
- **DAG Portfolio Mapping:** Links datasets, methods, and projects.
- **Gravity Propagation:** Simulates how reliability shocks attenuate through a network.
- **Interactive D3.js Dashboard:** Visualizes the collateral damage of a retraction event.

## Project Structure
- `core/math.py`: DAG propagation and shock calculation.
- `core/pipeline.py`: Scenario generation.
- `index.html`: Interactive impact dashboard.

## Target Journals
- *Journal of Clinical Epidemiology*
- *Research Integrity and Peer Review*
