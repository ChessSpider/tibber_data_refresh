"""Helpers for deriving electricity price snapshots from Tibber home data.

This module contains pure helper functions that transform Tibber API data
into Home Assistant–friendly structures for sensors and attributes.

No I/O or Home Assistant state is modified here.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from tibber.home import TibberHome


def build_energy_price_snapshot(home: TibberHome) -> dict[str, Any]:
    """Build a normalized energy price snapshot for a Tibber home.

    Exposes interval-based price data with currency and interval length,
    compatible with hourly and 15-minute markets.
    """
    price_total = home.price_total or {}
    tz = home._tibber_control.time_zone

    data: list[dict[str, Any]] = []
    timestamps: list[dt.datetime] = []

    for ts_str, price in sorted(price_total.items()):
        ts = dt.datetime.fromisoformat(ts_str).astimezone(tz)
        timestamps.append(ts)
        data.append(
            {
                "start_time": ts.isoformat(),
                "price_per_kwh": round(price, 4),
            }
        )

    interval_minutes: int | None = None
    if len(timestamps) >= 2:
        delta = timestamps[1] - timestamps[0]
        interval_minutes = int(delta.total_seconds() // 60)

    current_price, _current_time, price_rank = home.current_price_data()

    return {
        "current": current_price,
        "data": data,
        "currency": home.currency,
        "interval_minutes": interval_minutes,
        "price_rank": price_rank,
    }
