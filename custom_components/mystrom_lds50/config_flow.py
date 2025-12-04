"""Config flow for MyStrom LDS50 integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_MAC, CONF_NAME
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MyStromAPI, MyStromConnectionError
from .const import (
    CONF_DEVICE_TYPE,
    DOMAIN,
    ERROR_CANNOT_CONNECT,
    ERROR_UNKNOWN,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

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
    api = MyStromAPI(data[CONF_HOST], async_get_clientsession(hass))
    try:
        if not (report := await api.get_report()):
            msg = "Device did not return status report"
            raise CannotConnectError(msg)  # noqa: TRY301

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
    except MyStromConnectionError as err:
        msg = f"Cannot connect to device: {err}"
        raise CannotConnectError(msg) from err
    except Exception as err:
        _LOGGER.exception("Unexpected exception during validation")
        msg = f"Unexpected error: {err}"
        raise CannotConnectError(msg) from err
    else:
        return data


# Pylint incorrectly flags abstract method - is_matching is not required for all flows
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):  # pylint: disable=abstract-method
    """Handle a config flow for MyStrom LDS50."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ):
        """
        Handle the initial step.

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
            except CannotConnectError:
                errors["base"] = ERROR_CANNOT_CONNECT
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = ERROR_UNKNOWN

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnectError(HomeAssistantError):
    """Error to indicate we cannot connect."""
