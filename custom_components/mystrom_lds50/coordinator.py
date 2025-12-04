"""Data update coordinator for MyStrom devices."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import MyStromAPI, MyStromConnectionError
from .const import DEFAULT_SCAN_INTERVAL

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class MyStromDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for updating MyStrom device data."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,  # type: ignore[type-arg]
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"MyStrom {entry.title}",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.api = MyStromAPI(entry.data["host"], session=async_get_clientsession(hass))
        self.entry = entry

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the device."""
        try:
            if data := await self.api.get_report():
                return data
            msg = "Empty response from device"
            raise UpdateFailed(msg)
        except MyStromConnectionError as err:
            msg = f"Error communicating with device: {err}"
            raise UpdateFailed(msg) from err
