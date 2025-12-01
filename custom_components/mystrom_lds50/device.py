"""Device information helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers import device_registry as dr

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry


def get_device_info(entry: ConfigEntry) -> dr.DeviceInfo:  # type: ignore[type-arg]
    """Get device info for a config entry."""
    unique_id = entry.unique_id or entry.data.get("mac") or entry.data["host"]
    return dr.DeviceInfo(
        identifiers={(DOMAIN, unique_id)},
        name=entry.title,
        manufacturer="MyStrom",
        model=entry.data.get("device_type", "switch").title(),
    )
