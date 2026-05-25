# Retraction Gravity

[![ci](https://github.com/mahmood726-cyber/retraction-gravity/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/mahmood726-cyber/retraction-gravity/actions/workflows/ci.yml) [![codeql](https://github.com/mahmood726-cyber/retraction-gravity/actions/workflows/codeql.yml/badge.svg?branch=master)](https://github.com/mahmood726-cyber/retraction-gravity/actions/workflows/codeql.yml) [![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![python: 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

A Graph Theory and Bayesian Belief Network engine for mapping the impact of scientific retractions across a portfolio of medical research.

This project treats evidence as an interconnected Directed Acyclic Graph (DAG). If a dataset is retracted or a method is proven flawed, the "gravity" of that failure propagates to all dependent projects, dynamically updating their reliability scores.

## Features
- **DAG Portfolio Mapping:** Links datasets, methods, and projects.
- **Gravity Propagation:** Simulates how reliability shocks attenuate through a network.
- **Interactive D3.js Dashboard:** Visualizes the collateral damage of a retraction event.

## Project Structure
- `core/math.py`: DAG propagation and shock calculation.
- `core/pipeline.py`: Scenario generation.
- `core/test_pipeline.py`: Regression checks for repo-relative output and graph validation.
- `index.html`: Interactive impact dashboard.

## Verification
- `python -m unittest core.test_pipeline -q`

## Target Journals
- *Journal of Clinical Epidemiology*
- *Research Integrity and Peer Review*
