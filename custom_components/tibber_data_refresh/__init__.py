from __future__ import annotations

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    tibber_entry_id: str = entry.data["tibber_entry_id"]

    tibber_entry = hass.config_entries.async_get_entry(tibber_entry_id)
    if tibber_entry is None:
        raise ConfigEntryNotReady("Referenced Tibber config entry not found")

    if tibber_entry.state != config_entries.ConfigEntryState.LOADED:
        raise ConfigEntryNotReady("Tibber integration not loaded yet")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = tibber_entry.runtime_data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
