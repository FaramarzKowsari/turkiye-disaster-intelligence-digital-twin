from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx

AFAD_FILTER_URL = "https://deprem.afad.gov.tr/apiv2/event/filter"


def fetch_events(
    start: datetime,
    end: datetime,
    *,
    limit: int = 1000,
    min_lat: float | None = None,
    max_lat: float | None = None,
    min_lon: float | None = None,
    max_lon: float | None = None,
    timeout: float = 30.0,
) -> list[dict[str, Any]]:
    """Fetch earthquake events from AFAD's public event filtering service."""
    params: dict[str, Any] = {
        "start": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end.strftime("%Y-%m-%dT%H:%M:%S"),
        "limit": limit,
        "orderby": "timedesc",
    }
    optional = {
        "minlat": min_lat,
        "maxlat": max_lat,
        "minlon": min_lon,
        "maxlon": max_lon,
    }
    params.update({k: v for k, v in optional.items() if v is not None})

    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(AFAD_FILTER_URL, params=params)
        response.raise_for_status()
        payload = response.json()

    if isinstance(payload, list):
        return payload

    for key in ("eventList", "events", "data", "results"):
        value = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(value, list):
            return value

    raise ValueError("Unexpected AFAD response structure.")
