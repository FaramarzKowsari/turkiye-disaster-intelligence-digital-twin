import pandas as pd

from turkiye_disaster_twin.data.afad import normalise_events


def test_normalise_afad_records():
    records = [
        {
            "eventID": "evt-1",
            "date": "2026-08-10T12:30:00",
            "latitude": 40.9,
            "longitude": 29.1,
            "depth": 8.4,
            "type": "ML",
            "magnitude": 2.7,
            "location": "Marmara",
            "province": "İstanbul",
            "district": "Beykoz",
        }
    ]

    frame = normalise_events(records)

    assert list(frame["event_id"]) == ["evt-1"]
    assert frame.loc[0, "magnitude"] == 2.7
    assert frame.loc[0, "source"] == "AFAD"
    assert isinstance(frame.loc[0, "time_utc"], pd.Timestamp)
    assert str(frame.loc[0, "time_utc"].tz) == "UTC"


def test_normalise_empty_records_has_stable_schema():
    frame = normalise_events([])
    assert frame.empty
    assert {"event_id", "time_utc", "latitude", "longitude", "magnitude"} <= set(frame.columns)
