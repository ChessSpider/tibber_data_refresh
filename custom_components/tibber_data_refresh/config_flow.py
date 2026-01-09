from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult

from .const import DOMAIN, TIBBER_DOMAIN

_LOGGER = logging.getLogger(__name__)


class TibberDataRefreshConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for tibber_data_refresh."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        tibber_entries = self.hass.config_entries.async_entries(TIBBER_DOMAIN)

        if not tibber_entries:
            return self.async_abort(reason="tibber_not_configured")

        existing_entry_ids: set[str] = {
            entry.data["tibber_entry_id"]
            for entry in self._async_current_entries()
            if "tibber_entry_id" in entry.data
        }

        choices: dict[str, str] = {
            entry.entry_id: entry.title
            for entry in tibber_entries
            if entry.entry_id not in existing_entry_ids
        }

        if not choices:
            return self.async_abort(reason="already_configured")

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {vol.Required("tibber_entry_id"): vol.In(choices)}
                ),
            )

        tibber_entry_id: str = user_input["tibber_entry_id"]

        tibber_entry = self.hass.config_entries.async_get_entry(tibber_entry_id)
        if tibber_entry is None:
            return self.async_abort(reason="tibber_entry_missing")

        return self.async_create_entry(
            title=f"Tibber Data Refresh ({tibber_entry.title})",
            data={"tibber_entry_id": tibber_entry_id},
        )
