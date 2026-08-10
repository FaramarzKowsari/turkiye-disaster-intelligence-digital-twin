from __future__ import annotations

import json
from datetime import datetime

import typer

from turkiye_disaster_twin.config import ISTANBUL_BOUNDS
from turkiye_disaster_twin.data.afad import fetch_events

app = typer.Typer(help="Türkiye Disaster Intelligence Digital Twin CLI")


@app.command()
def afad(
    start: str = typer.Option(..., help="ISO datetime, e.g. 2026-01-01T00:00:00"),
    end: str = typer.Option(..., help="ISO datetime, e.g. 2026-01-31T23:59:59"),
    limit: int = typer.Option(100, min=1, max=10000),
):
    """Fetch AFAD events in the broad İstanbul pilot bounding box."""
    events = fetch_events(
        datetime.fromisoformat(start),
        datetime.fromisoformat(end),
        limit=limit,
        min_lat=ISTANBUL_BOUNDS.min_lat,
        max_lat=ISTANBUL_BOUNDS.max_lat,
        min_lon=ISTANBUL_BOUNDS.min_lon,
        max_lon=ISTANBUL_BOUNDS.max_lon,
    )
    typer.echo(json.dumps(events, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
