"""Device information helpers."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN


def get_device_info(entry: ConfigEntry) -> dr.DeviceInfo:
    """Get device info for a config entry."""
    unique_id = entry.unique_id or entry.data.get("mac") or entry.data["host"]
    return dr.DeviceInfo(
        identifiers={(DOMAIN, unique_id)},
        name=entry.title,
        manufacturer="MyStrom",
        model=entry.data.get("device_type", "switch").title(),
    )

