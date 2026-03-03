"""Sensor platform for exposing Tibber electricity price data.

This module defines a Home Assistant sensor entity that represents the current
electricity price for a Tibber home, including detailed price attributes for
today and tomorrow derived from Tibber price data.
"""

from __future__ import annotations

from datetime import timedelta

from tibber import Tibber
from tibber.home import TibberHome

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.tibber import TibberRuntimeData
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .price_helpers import build_energy_price_snapshot

SCAN_INTERVAL = timedelta(hours=1)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up electricity price sensors for a Tibber config entry.

    One sensor is created per active Tibber home with an active subscription.
    """
    runtime_data: TibberRuntimeData = hass.data[DOMAIN][entry.entry_id]
    tibber_connection: Tibber = runtime_data.async_get_client(hass)

    entities: list[TibberEnergyPriceSensor] = []

    for home in tibber_connection.get_homes(only_active=True):
        if not home.has_active_subscription:
            continue
        entities.append(TibberEnergyPriceSensor(runtime_data, home))

    async_add_entities(entities, update_before_add=True)


class TibberEnergyPriceSensor(SensorEntity):
    """Sensor representing the current electricity price for a Tibber home.

    The sensor exposes the current total electricity price as its native value,
    and provides additional attributes with detailed price information for
    today and tomorrow.
    """

    _attr_has_entity_name = True
    _attr_translation_key = "electricity_price"

    def __init__(self, runtime_data: TibberRuntimeData, home: TibberHome) -> None:
        """Initialize the electricity price sensor.

        Args:
            runtime_data: The runtime data for the Tibber integration.
            home: The Tibber home this sensor represents.
        """
        self._runtime_data = runtime_data
        self._home = home

        self._attr_unique_id = f"{home.home_id}_energy_price"
        self._attr_native_unit_of_measurement = home.price_unit

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, home.home_id)},
            name=home.name,
            manufacturer="Tibber",
            model="Electricity price",
        )

    async def async_update(self) -> None:
        """Zorg dat price_total up-to-date is."""

        self._runtime_data.async_get_client(
            self.hass
        )  # dumb code to refresh access token if needed before updating price info
        await self._home.update_info_and_price_info()

        snapshot = build_energy_price_snapshot(self._home)
        self._attr_native_value = snapshot["current"]
        self._attr_extra_state_attributes = {
            "data": snapshot["data"],
            "currency": snapshot["currency"],
            "interval_minutes": snapshot["interval_minutes"],
            "price_rank": snapshot["price_rank"],
        }
        self._attr_available = snapshot["current"] is not None
