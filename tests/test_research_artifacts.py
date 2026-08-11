from pathlib import Path

import pandas as pd

from turkiye_disaster_twin.research.artifacts import (
    runtime_metadata,
    write_experiment_bundle,
)


def test_csv_bundle_and_checksums(tmp_path: Path):
    frame = pd.DataFrame(
        [{"severity_control": 0.25, "algorithm": "greedy", "value": 1.0}]
    )
    metadata = runtime_metadata({"test_run": True})

    outputs = write_experiment_bundle(
        tmp_path,
        raw=frame,
        exploratory_summary=frame,
        paired_inference=frame,
        metadata=metadata,
        require_parquet=False,
    )

    assert outputs["raw_experiments_csv"].exists()
    assert outputs["manifest"].exists()
    assert outputs["checksums"].exists()

    checksum_text = outputs["checksums"].read_text(encoding="utf-8")
    assert "raw_experiments.csv" in checksum_text
    assert "manifest.json" in checksum_text
