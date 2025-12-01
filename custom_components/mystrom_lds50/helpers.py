"""Helper functions for MyStrom integration."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from .const import DOMAIN
from .coordinator import MyStromDataUpdateCoordinator


def get_coordinator_from_entity_id(
    hass: HomeAssistant, entity_id: str
) -> MyStromDataUpdateCoordinator | None:
    """Get coordinator from entity ID.

    Args:
        hass: Home Assistant instance
        entity_id: Entity ID

    Returns:
        Coordinator if found, None otherwise
    """
    entity_registry = er.async_get(hass)
    if (entity_entry := entity_registry.async_get(entity_id)) is None:
        return None

    device_registry = dr.async_get(hass)
    if (device_entry := device_registry.async_get(entity_entry.device_id)) is None:
        return None

    config_entry_id = next(iter(device_entry.config_entries), None)
    if config_entry_id is None:
        return None

    return hass.data.get(DOMAIN, {}).get(config_entry_id)

