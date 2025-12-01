"""Sensor platform for MyStrom devices."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_WIFI_SIGNAL,
    DOMAIN,
    KEY_ENERGY,
    KEY_POWER,
    KEY_TEMPERATURE,
    KEY_WS,
)
from .coordinator import MyStromDataUpdateCoordinator
from .device import get_device_info

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MyStrom sensors from a config entry.

    Args:
        hass: Home Assistant instance
        entry: Configuration entry
        async_add_entities: Callback to add entities
    """
    coordinator: MyStromDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors: list[SensorEntity] = []

    # Power sensor
    sensors.append(MyStromPowerSensor(coordinator, entry))

    # Temperature sensor (if available)
    if coordinator.data and KEY_TEMPERATURE in coordinator.data:
        sensors.append(MyStromTemperatureSensor(coordinator, entry))

    # Energy sensor (if available)
    if coordinator.data and KEY_ENERGY in coordinator.data:
        sensors.append(MyStromEnergySensor(coordinator, entry))

    async_add_entities(sensors)


class MyStromSensorBase(
    CoordinatorEntity[MyStromDataUpdateCoordinator], SensorEntity
):
    """Base class for MyStrom sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MyStromDataUpdateCoordinator,
        entry: ConfigEntry,
        sensor_key: str,
        unique_id_suffix: str,
    ) -> None:
        """Initialize the sensor.

        Args:
            coordinator: Data update coordinator
            entry: Configuration entry
            sensor_key: Key in coordinator data
            unique_id_suffix: Suffix for unique ID
        """
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._entry = entry
        unique_id_base = (
            entry.unique_id or entry.data.get("mac") or entry.data["host"]
        )
        self._attr_unique_id = f"{unique_id_base}_{unique_id_suffix}"
        self._attr_device_info = get_device_info(entry)


class MyStromPowerSensor(MyStromSensorBase):
    """Representation of a MyStrom power sensor."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_name = "Power"

    def __init__(
        self,
        coordinator: MyStromDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the power sensor.

        Args:
            coordinator: Data update coordinator
            entry: Configuration entry
        """
        super().__init__(coordinator, entry, KEY_POWER, "power")

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor.

        Returns:
            Current power consumption in watts
        """
        if not self.coordinator.data:
            return None

        if (power := self.coordinator.data.get(KEY_POWER)) is None:
            return None

        try:
            return float(power)
        except (ValueError, TypeError):
            return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes.

        Returns:
            Dictionary of state attributes
        """
        if not self.coordinator.data:
            return {}

        attrs: dict[str, Any] = {}

        # WiFi signal strength
        if KEY_WS in self.coordinator.data:
            attrs[ATTR_WIFI_SIGNAL] = self.coordinator.data[KEY_WS]

        return attrs


class MyStromTemperatureSensor(MyStromSensorBase):
    """Representation of a MyStrom temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_name = "Temperature"

    def __init__(
        self,
        coordinator: MyStromDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the temperature sensor.

        Args:
            coordinator: Data update coordinator
            entry: Configuration entry
        """
        super().__init__(coordinator, entry, KEY_TEMPERATURE, "temperature")

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor.

        Returns:
            Current temperature in Celsius
        """
        if not self.coordinator.data:
            return None

        if (temp := self.coordinator.data.get(KEY_TEMPERATURE)) is None:
            return None

        try:
            return float(temp)
        except (ValueError, TypeError):
            return None


class MyStromEnergySensor(MyStromSensorBase):
    """Representation of a MyStrom energy sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_name = "Energy"

    def __init__(
        self,
        coordinator: MyStromDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the energy sensor.

        Args:
            coordinator: Data update coordinator
            entry: Configuration entry
        """
        super().__init__(coordinator, entry, KEY_ENERGY, "energy")

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor.

        Returns:
            Total energy consumption in kWh
        """
        if not self.coordinator.data:
            return None

        if (energy := self.coordinator.data.get(KEY_ENERGY)) is None:
            return None

        try:
            # Convert from Wh to kWh if needed
            if (energy_value := float(energy)) > 1000:
                return energy_value / 1000.0
            return energy_value
        except (ValueError, TypeError):
            return None
