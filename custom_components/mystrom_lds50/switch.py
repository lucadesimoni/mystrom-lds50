"""Switch platform for MyStrom devices."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_DEVICE_TYPE,
    ATTR_HOST,
    ATTR_MAC,
    ATTR_POWER,
    DOMAIN,
    KEY_POWER,
    KEY_RELAY,
)
from .coordinator import MyStromDataUpdateCoordinator
from .device import get_device_info

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,  # type: ignore[type-arg]
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MyStrom switches from a config entry."""
    coordinator: MyStromDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MyStromSwitch(coordinator, entry)])


# Pylint incorrectly flags abstract methods - async_turn_on/off are implemented
class MyStromSwitch(CoordinatorEntity[MyStromDataUpdateCoordinator], SwitchEntity):  # pylint: disable=abstract-method
    """Representation of a MyStrom switch."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(
        self,
        coordinator: MyStromDataUpdateCoordinator,
        entry: ConfigEntry,  # type: ignore[type-arg]
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._entry = entry
        unique_id_base = (
            entry.unique_id or entry.data.get("mac") or entry.data["host"]
        )
        self._attr_unique_id = unique_id_base
        self._attr_device_info = get_device_info(entry)

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        if not self.coordinator.data:
            return False
        if (relay := self.coordinator.data.get(KEY_RELAY)) is not None:
            return bool(relay)
        return bool(self.coordinator.data.get(KEY_POWER, 0) > 0)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.coordinator.api.turn_on()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.coordinator.api.turn_off()
        await self.coordinator.async_request_refresh()

    async def async_toggle(self, **kwargs: Any) -> None:
        """Toggle the switch."""
        await self.coordinator.api.toggle_relay()
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}

        attrs: dict[str, Any] = {
            ATTR_HOST: self._entry.data["host"],
            ATTR_DEVICE_TYPE: self._entry.data.get("device_type", "switch"),
        }

        if mac := self.coordinator.data.get("mac"):
            attrs[ATTR_MAC] = mac
        if power := self.coordinator.data.get(KEY_POWER):
            attrs[ATTR_POWER] = power

        return attrs
