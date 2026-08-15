# Reproducibility — v1.0


## Persistent identifiers

The frozen software release is archived at Zenodo with **version DOI
[10.5281/zenodo.21903851](https://doi.org/10.5281/zenodo.21903851)**. The project-level
**Concept DOI [10.5281/zenodo.21903850](https://doi.org/10.5281/zenodo.21903850)** represents all
versions of the research software record.

## Frozen evidence chain

The final confirmatory interpretation is anchored to two GitHub Actions runs:

| Purpose | Run ID | Commit |
|---|---:|---|
| Primary fine-grid confirmatory run | `31582171618` | `8078af69eff047d7da71beac3b5b3b125a121d1a` |
| Upper-bound extension | `31585895864` | `8078af69eff047d7da71beac3b5b3b125a121d1a` |

Both runs used base seed `7070`.

The v0.8 freeze preserved:

- final boundary tables
- extended service-probability curves
- publication figures
- source GitHub Actions artifact ZIPs
- a frozen JSON manifest
- SHA-256 checksums

under `results/final_v0.8/`.

## Primary estimand

The primary reliability-boundary quantity is the synthetic severity control value at which

`P(reachability >= 80%) = 80%`.

The curve is regularized to be non-increasing before the crossing is estimated. Uncertainty is
computed by resampling complete stochastic worlds, preserving within-world coupling across
severity.

## Reproducing software tests

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev,app,research]"
ruff check .
python -m compileall -q src app scripts tests
pytest
```

## Re-running research workflows

The repository retains three manually executable research workflows:

- `Research Benchmark`
- `Coupled Phase Boundary Benchmark`
- `Confirmatory Reliability Boundary Benchmark`

Re-running them may produce a new artifact and a new run ID. Such a run does not silently replace
the frozen v1.0 evidence. A new scientific release should explicitly record and review any changed
result.

## Integrity verification

From the repository root:

```bash
cd results/final_v0.8
sha256sum -c SHA256SUMS
```

On systems without `sha256sum`, hashes can be checked with Python's `hashlib`.

## Interpretation boundary

The experiment is computational and synthetic. Reproducibility means that the research software
and numerical experiment can be independently rerun; it does not imply operational validation of
earthquake damage or emergency-service performance.
