"""Custom services for MyStrom devices."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, SERVICE_REBOOT, SERVICE_SET_RELAY_STATE, SERVICE_TOGGLE_RELAY
from .helpers import get_coordinator_from_entity_id

_LOGGER = logging.getLogger(__name__)

SERVICE_SET_RELAY_STATE_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Required("state"): cv.boolean,
    }
)

SERVICE_TOGGLE_RELAY_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)

SERVICE_REBOOT_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up custom services."""
    if hass.services.has_service(DOMAIN, SERVICE_SET_RELAY_STATE):
        return

    async def handle_set_relay_state(call: ServiceCall) -> None:
        """Handle set_relay_state service call."""
        coordinator = get_coordinator_from_entity_id(
            hass, call.data["entity_id"]
        )
        if not coordinator:
            _LOGGER.error("Entity %s not found", call.data["entity_id"])
            return

        await coordinator.api.set_relay(call.data["state"])
        await coordinator.async_request_refresh()

    async def handle_toggle_relay(call: ServiceCall) -> None:
        """Handle toggle_relay service call."""
        coordinator = get_coordinator_from_entity_id(
            hass, call.data["entity_id"]
        )
        if not coordinator:
            _LOGGER.error("Entity %s not found", call.data["entity_id"])
            return

        await coordinator.api.toggle_relay()
        await coordinator.async_request_refresh()

    async def handle_reboot(call: ServiceCall) -> None:
        """Handle reboot service call."""
        coordinator = get_coordinator_from_entity_id(
            hass, call.data["entity_id"]
        )
        if not coordinator:
            _LOGGER.error("Entity %s not found", call.data["entity_id"])
            return

        await coordinator.api.reboot()

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_RELAY_STATE,
        handle_set_relay_state,
        schema=SERVICE_SET_RELAY_STATE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_TOGGLE_RELAY,
        handle_toggle_relay,
        schema=SERVICE_TOGGLE_RELAY_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_REBOOT,
        handle_reboot,
        schema=SERVICE_REBOOT_SCHEMA,
    )
