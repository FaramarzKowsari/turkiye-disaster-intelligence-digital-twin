from __future__ import annotations

import json
import platform
import sys
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

import pandas as pd


def runtime_metadata(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return reproducibility metadata for an experiment bundle."""
    metadata: dict[str, Any] = {
        "created_at_utc": datetime.now(UTC).isoformat(),
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "schema_version": "paper-grade-v0.4",
    }
    if extra:
        metadata.update(extra)
    return metadata


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_frame(
    frame: pd.DataFrame,
    stem: Path,
    *,
    require_parquet: bool,
) -> list[Path]:
    written: list[Path] = []

    csv_path = stem.with_suffix(".csv")
    frame.to_csv(csv_path, index=False)
    written.append(csv_path)

    parquet_path = stem.with_suffix(".parquet")
    try:
        frame.to_parquet(parquet_path, index=False)
        written.append(parquet_path)
    except (ImportError, ModuleNotFoundError, ValueError):
        if require_parquet:
            raise RuntimeError(
                "Parquet export requires the research extra: "
                'pip install -e ".[research]"'
            ) from None

    return written


def write_experiment_bundle(
    output_dir: str | Path,
    *,
    raw: pd.DataFrame,
    exploratory_summary: pd.DataFrame,
    paired_inference: pd.DataFrame,
    metadata: dict[str, Any],
    require_parquet: bool = True,
) -> dict[str, Path]:
    """Write a versioned research artifact bundle with SHA-256 checksums."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    named_paths: dict[str, Path] = {}

    tables = {
        "raw_experiments": raw,
        "exploratory_summary": exploratory_summary,
        "paired_inference": paired_inference,
    }
    for name, frame in tables.items():
        table_paths = _write_frame(
            frame,
            destination / name,
            require_parquet=require_parquet,
        )
        written.extend(table_paths)
        named_paths.update(
            {f"{name}_{path.suffix.lstrip('.')}": path for path in table_paths}
        )

    manifest_path = destination / "manifest.json"
    manifest_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    written.append(manifest_path)
    named_paths["manifest"] = manifest_path

    checksums_path = destination / "SHA256SUMS"
    checksum_lines = [
        f"{_sha256(path)}  {path.name}"
        for path in sorted(written, key=lambda item: item.name)
    ]
    checksums_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    named_paths["checksums"] = checksums_path

    return named_paths
