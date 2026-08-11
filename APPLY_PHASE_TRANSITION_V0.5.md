# Apply v0.5 — Severity × Responder Phase-Transition Study

1. Extract this ZIP directly into the repository root.
2. Allow replacement of:
   - `pyproject.toml`
   - `.github/workflows/research-benchmark.yml`
3. New files include:
   - `.github/workflows/phase-transition-benchmark.yml`
   - `scripts/run_phase_transition_benchmark.py`
   - `src/turkiye_disaster_twin/simulation/phase_transition.py`
   - `src/turkiye_disaster_twin/research/phase_artifacts.py`
   - `tests/test_phase_transition.py`
   - `docs/phase_transition_study.md`
   - `results/benchmark_001/*`
4. Open GitHub Desktop.
5. Commit with:

   `Add phase-transition study and preserve Benchmark 001 evidence`

6. Push origin.
7. Wait for CI and GitHub Pages.

After CI is green, a new workflow appears:

**Actions → Phase Transition Benchmark**

Recommended first run:

- Place: Beykoz, İstanbul, Türkiye
- Realisations per grid cell: 25
- Severities: 0.05,0.10,0.15,0.20,0.25,0.30
- Responders: 4,6,8,10,12,16
- Incidents: 10
- Base seed: 4040

The 25-realisation run is intentionally the first grid test. Increase to 50 or 100 only after
measuring runtime and confirming the frontier outputs are informative.
