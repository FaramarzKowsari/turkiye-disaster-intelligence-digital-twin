from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx
import pandas as pd

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
    """Fetch earthquake events from AFAD's public filtering endpoint."""
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
    params.update({key: value for key, value in optional.items() if value is not None})

    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(AFAD_FILTER_URL, params=params)
        response.raise_for_status()
        payload = response.json()

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        for key in ("eventList", "events", "data", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return value

    raise ValueError("Unexpected AFAD response structure.")


def normalise_events(records: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert heterogeneous AFAD records into the project's stable event schema."""
    columns = [
        "event_id",
        "time_utc",
        "latitude",
        "longitude",
        "depth_km",
        "magnitude",
        "magnitude_type",
        "location",
        "province",
        "district",
        "source",
    ]
    if not records:
        return pd.DataFrame(columns=columns)

    raw = pd.DataFrame.from_records(records)

    aliases = {
        "event_id": ("eventID", "eventId", "eventid", "id"),
        "time_utc": ("date", "time", "datetime"),
        "latitude": ("latitude", "lat"),
        "longitude": ("longitude", "lon", "lng"),
        "depth_km": ("depth", "depth_km"),
        "magnitude": ("magnitude", "mag"),
        "magnitude_type": ("type", "magnitudeType", "magType"),
        "location": ("location", "place"),
        "province": ("province", "city"),
        "district": ("district",),
    }

    frame = pd.DataFrame(index=raw.index)
    for target, candidates in aliases.items():
        source = next((name for name in candidates if name in raw.columns), None)
        frame[target] = raw[source] if source is not None else pd.NA

    frame["time_utc"] = pd.to_datetime(frame["time_utc"], errors="coerce", utc=True)
    for column in ("latitude", "longitude", "depth_km", "magnitude"):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame["source"] = "AFAD"
    return frame[columns]


def fetch_events_frame(
    start: datetime,
    end: datetime,
    *,
    min_magnitude: float | None = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """Fetch, normalise, and optionally filter AFAD events by magnitude.

    Magnitude filtering is intentionally performed client-side so the project does
    not depend on an undocumented or version-specific AFAD magnitude parameter name.
    """
    frame = normalise_events(fetch_events(start, end, **kwargs))
    if min_magnitude is not None and not frame.empty:
        frame = frame[frame["magnitude"] >= float(min_magnitude)].copy()
    return frame.reset_index(drop=True)
