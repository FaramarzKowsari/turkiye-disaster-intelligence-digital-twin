# Apply v0.6 — Coupled Phase Boundary Design

1. Extract this ZIP directly into the repository root.
2. Allow replacement of:
   - `src/turkiye_disaster_twin/simulation/phase_transition.py`
   - `scripts/run_phase_transition_benchmark.py`
   - `tests/test_phase_transition.py`
   - `.github/workflows/phase-transition-benchmark.yml`
   - `pyproject.toml`
3. New evidence is added under:
   - `results/phase_transition_002/`
   - `docs/coupled_severity_design.md`
4. Open GitHub Desktop.
5. Commit with:

   `Couple severity worlds and preserve Phase Benchmark 002`

6. Push origin and wait for CI.

After CI is green, the workflow appears as:

**Actions → Coupled Phase Boundary Benchmark**

Recommended confirmatory run:

- Place: `Beykoz, İstanbul, Türkiye`
- Realisations: `100`
- Severities: `0.10,0.12,0.13,0.14,0.15,0.16,0.18,0.20`
- Responders: `8,10,12,14,16,20,24,32`
- Incidents: `10`
- Base seed: `6060`

The v0.6 engine reuses the same stochastic world across all severity values in each realisation.
