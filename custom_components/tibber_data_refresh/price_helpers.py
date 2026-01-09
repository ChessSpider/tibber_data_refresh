"""Helpers for deriving electricity price snapshots from Tibber home data.

This module contains pure helper functions that transform Tibber API data
into Home Assistant–friendly structures for sensors and attributes.

No I/O or Home Assistant state is modified here.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

from tibber.home import TibberHome

from homeassistant.util import dt as dt_util


def build_energy_price_snapshot(home: TibberHome) -> dict[str, Any]:
    """Build a snapshot of electricity price information for a Tibber home.

    The snapshot is derived from ``TibberHome.price_total`` and represents
    total electricity prices (including grid fees and taxes) for today and
    tomorrow, as provided by Tibber.

    The returned structure is designed to be used directly by a Home Assistant
    sensor, with the current price as the native value and the remaining fields
    exposed as extra state attributes.

    Args:
        home: A ``TibberHome`` instance with populated price data.

    Returns:
        A dictionary containing:
        - ``current``: Current total electricity price, or ``None``.
        - ``today``: List of total prices for today (chronological order).
        - ``raw_today``: List of dicts with ``time`` and ``total`` for today.
        - ``tomorrow``: List of total prices for tomorrow.
        - ``raw_tomorrow``: List of dicts with ``time`` and ``total`` for tomorrow.
        - ``tomorrow_valid``: ``True`` if tomorrow prices are available.
        - ``price_rank``: Relative rank (0–1) of the current price within today.
        - ``cheapest_today``: Dict with ``time`` and ``total`` for the cheapest
          price today, or ``None``.
    """
    price_total = home.price_total or {}

    tz = home._tibber_control.time_zone
    now = dt_util.now(tz)
    today_date = now.date()
    tomorrow_date = today_date + dt.timedelta(days=1)

    today: list[float] = []
    tomorrow: list[float] = []
    raw_today: list[dict[str, Any]] = []
    raw_tomorrow: list[dict[str, Any]] = []

    # Sort explicitly to guarantee chronological order
    for ts_str, price in sorted(price_total.items()):
        ts = dt.datetime.fromisoformat(ts_str).astimezone(tz)

        entry = {
            "time": ts_str,
            "total": price,
        }

        if ts.date() == today_date:
            today.append(price)
            raw_today.append(entry)
        elif ts.date() == tomorrow_date:
            tomorrow.append(price)
            raw_tomorrow.append(entry)

    current_price, _current_time, price_rank = home.current_price_data()

    return {
        "current": current_price,
        "today": today,
        "raw_today": raw_today,
        "tomorrow": tomorrow,
        "raw_tomorrow": raw_tomorrow,
        "tomorrow_valid": bool(tomorrow),
        "price_rank": price_rank,
        "cheapest_today": min(raw_today, key=lambda x: x["total"])
        if raw_today
        else None,
    }
