from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
from typing import Any

import pandas as pd


def _hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_table(
    destination: Path,
    name: str,
    frame: pd.DataFrame,
) -> list[Path]:
    csv_path = destination / f"{name}.csv"
    parquet_path = destination / f"{name}.parquet"

    frame.to_csv(csv_path, index=False)
    frame.to_parquet(parquet_path, index=False)
    return [csv_path, parquet_path]


def write_phase_transition_bundle(
    output_dir: str | Path,
    *,
    raw: pd.DataFrame,
    surface: pd.DataFrame,
    frontier: pd.DataFrame,
    marginal_gains: pd.DataFrame,
    paired_inference: pd.DataFrame,
    metadata: dict[str, Any],
) -> dict[str, Path]:
    """Write all v0.5 phase-transition research products with checksums."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    tables = {
        "raw_phase_experiments": raw,
        "phase_surface": surface,
        "resource_frontier": frontier,
        "marginal_resource_gains": marginal_gains,
        "paired_grid_inference": paired_inference,
    }

    written: list[Path] = []
    outputs: dict[str, Path] = {}

    for name, frame in tables.items():
        for path in _write_table(destination, name, frame):
            written.append(path)
            outputs[f"{name}_{path.suffix.lstrip('.')}"] = path

    manifest_path = destination / "manifest.json"
    manifest_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    written.append(manifest_path)
    outputs["manifest"] = manifest_path

    checksums_path = destination / "SHA256SUMS"
    checksums = [
        f"{_hash(path)}  {path.name}"
        for path in sorted(written, key=lambda value: value.name)
    ]
    checksums_path.write_text("\n".join(checksums) + "\n", encoding="utf-8")
    outputs["checksums"] = checksums_path

    return outputs
