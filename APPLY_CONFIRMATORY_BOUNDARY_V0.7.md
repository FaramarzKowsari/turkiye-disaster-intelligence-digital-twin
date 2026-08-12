# Apply v0.7 — Confirmatory Reliability Boundary Study

1. Extract this ZIP directly into the repository root.
2. Allow replacement of:
   - `src/turkiye_disaster_twin/research/phase_artifacts.py`
   - `pyproject.toml`
3. New files include:
   - `src/turkiye_disaster_twin/research/boundary.py`
   - `scripts/run_confirmatory_boundary_benchmark.py`
   - `.github/workflows/confirmatory-boundary-benchmark.yml`
   - `tests/test_boundary_estimation.py`
   - `docs/confirmatory_boundary_design.md`
   - `results/coupled_phase_boundary_003/*`
4. Open GitHub Desktop.
5. Commit with:

   `Add confirmatory reliability-boundary inference v0.7`

6. Push origin and wait for CI.

After CI is green, run:

**Actions → Confirmatory Reliability Boundary Benchmark**

Recommended first confirmatory run:

- Place: Beykoz, İstanbul, Türkiye
- Realisations: 300
- Severities: 0.130,0.135,0.140,0.145,0.150,0.1525,0.155,0.1575,0.160,0.1625,0.165
- Responders: 12,14,16,20,24,32
- Incidents: 10
- Base seed: 7070
- Boundary bootstrap resamples: 5000

Do not rerun an older workflow attempt; launch a new run from the v0.7 workflow.
