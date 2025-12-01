"""Config flow for MyStrom LDS50 integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_MAC, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .api import MyStromAPI, MyStromConnectionError
from .const import (
    CONF_DEVICE_TYPE,
    DOMAIN,
    ERROR_CANNOT_CONNECT,
    ERROR_UNKNOWN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_NAME): str,
        vol.Optional(CONF_MAC): str,
        vol.Optional(CONF_DEVICE_TYPE, default="switch"): vol.In(
            ["switch", "zero", "bulb", "button"]
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    from homeassistant.helpers.aiohttp_client import async_get_clientsession

    api = MyStromAPI(data[CONF_HOST], async_get_clientsession(hass))
    try:
        if not (report := await api.get_report()):
            raise CannotConnect("Device did not return status report")

        # Extract MAC from report if not provided
        if not data.get(CONF_MAC) and (mac := report.get("mac")):
            data[CONF_MAC] = mac

        # Extract device type from report if available
        if device_type := report.get("type"):
            device_type_map = {
                "Switch": "switch",
                "Zero": "zero",
                "Bulb": "bulb",
                "Button": "button",
            }
            if mapped_type := device_type_map.get(device_type):
                data[CONF_DEVICE_TYPE] = mapped_type

        return data
    except MyStromConnectionError as err:
        raise CannotConnect(f"Cannot connect to device: {err}") from err
    except Exception as err:
        _LOGGER.exception("Unexpected exception during validation")
        raise CannotConnect(f"Unexpected error: {err}") from err


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MyStrom LDS50."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step.

        Args:
            user_input: User input data

        Returns:
            Flow result
        """
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                validated_data = await validate_input(self.hass, user_input)
                device_name = validated_data.get(CONF_NAME) or validated_data[CONF_HOST]
                mac = validated_data.get(CONF_MAC) or validated_data[CONF_HOST]

                # Check if already configured
                await self.async_set_unique_id(mac)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=device_name,
                    data=validated_data,
                )
            except CannotConnect:
                errors["base"] = ERROR_CANNOT_CONNECT
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = ERROR_UNKNOWN

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

