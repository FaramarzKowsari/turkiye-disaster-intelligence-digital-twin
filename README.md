# Türkiye Disaster Intelligence Digital Twin

**Research-grade open-source decision-support testbed for earthquake response in İstanbul, designed to scale to Türkiye.**

## Research question

> Under uncertain post-earthquake road disruption and emergency demand, can graph-aware resource allocation reduce critical response time and unmet demand compared with static shortest-path and greedy dispatch baselines?

This repository is deliberately designed as a **research system**, not merely a dashboard.

## Why this project

Türkiye faces high earthquake risk, while emergency response is a coupled problem involving:

- seismic events,
- road-network accessibility,
- hospitals and emergency facilities,
- uncertain incident demand,
- limited response resources,
- cascading network disruption,
- dynamic decisions under uncertainty.

The initial pilot focuses on **İstanbul**. The architecture is city-agnostic and can later expand to other provinces.

## Version roadmap

### v0.1 — Reproducible earthquake-response simulator
- AFAD earthquake event ingestion
- OpenStreetMap road-network ingestion
- hospitals / fire stations / emergency facilities from OSM
- synthetic post-earthquake road disruption scenarios
- synthetic emergency-demand generator
- baseline dispatch algorithms
- evaluation metrics
- reproducible CLI + tests

### v0.2 — Spatial hazard and vulnerability
- shaking / intensity proxy layer
- district-level vulnerability features
- calibrated edge-failure scenarios
- uncertainty quantification
- Monte Carlo scenario engine

### v0.3 — Optimization
- min-cost flow / capacitated assignment
- multi-objective optimization
- hospital-capacity constraints
- fairness / vulnerable-area penalties

### v0.4 — Multi-Agent Reinforcement Learning
- PettingZoo-compatible environment
- PPO / MAPPO baselines
- centralized training, decentralized execution
- robustness to missing and delayed observations

### v0.5 — Digital-twin interface
- FastAPI backend
- PostGIS
- interactive map
- scenario playback
- explainable dispatch recommendations
- experiment comparison

### v1.0 — Paper-grade release
- ablation studies
- uncertainty analysis
- reproducibility package
- benchmark dataset
- technical paper / preprint
- DOI-ready release

## Data principles

We prefer:
1. official Turkish public sources,
2. open and reproducible data,
3. zero dependency on paid AI APIs,
4. explicit licensing and provenance,
5. synthetic data only when real operational data are unavailable.

### Initial sources

- **AFAD Earthquake Event Web Service**  
  https://deprem.afad.gov.tr/event-service

- **OpenStreetMap** for roads and public facilities  
  https://www.openstreetmap.org/

- **Republic of Türkiye Ministry of Health Open Data Portal**  
  https://acikveri.saglik.gov.tr/

- **National Smart Cities Open Data Platform**  
  https://ulasav.csb.gov.tr/

## Scientific integrity

The early simulator does **not** claim to predict real building collapse or real road failure.
Until calibrated hazard/vulnerability models are introduced, damaged roads and emergency
demand are generated as controlled stochastic scenarios. Every simulated field is labeled
as synthetic in outputs.

## Core metrics

- mean response time
- median response time
- p90 critical response time
- weighted unmet demand
- percentage of incidents reachable
- hospital overload
- disconnected population / demand proxy
- network resilience ratio
- dispatch distance
- fairness gap across districts

## Repository structure

```text
.
├── src/turkiye_disaster_twin/
│   ├── data/
│   │   ├── afad.py
│   │   └── osm.py
│   ├── simulation/
│   │   ├── scenario.py
│   │   └── baselines.py
│   ├── config.py
│   └── cli.py
├── tests/
├── docs/
│   ├── research_protocol.md
│   └── data_sources.md
├── .github/workflows/ci.yml
├── pyproject.toml
└── CITATION.cff
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate  # Windows

pip install -e ".[dev]"

disaster-twin afad   --start "2026-01-01T00:00:00"   --end "2026-01-31T23:59:59"   --limit 100

pytest
```

## Baselines before deep learning

No RL model will be accepted as useful unless it beats transparent baselines:

1. nearest available responder,
2. shortest-travel-time greedy dispatch,
3. capacitated minimum-cost assignment,
4. static pre-positioning heuristic.

This prevents the common mistake of using deep learning where a simple algorithm is already better.

## Proposed paper title

**A Graph-Aware Digital Twin for Uncertain Post-Earthquake Emergency Response in İstanbul**

## Author

Faramarz Kowsari

## Status

Research prototype — not an operational emergency system.
