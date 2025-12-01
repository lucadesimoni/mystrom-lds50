"""Tests for MyStrom sensor platform."""

from unittest.mock import MagicMock

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mystrom_lds50.const import (
    DOMAIN,
    KEY_ENERGY,
    KEY_POWER,
    KEY_TEMPERATURE,
)
from custom_components.mystrom_lds50.coordinator import MyStromDataUpdateCoordinator
from custom_components.mystrom_lds50.sensor import (
    MyStromEnergySensor,
    MyStromPowerSensor,
    MyStromTemperatureSensor,
)


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={
            "host": "192.168.1.100",
            "mac": "AA:BB:CC:DD:EE:FF",
            "name": "MyStrom Switch",
            "device_type": "switch",
        },
        unique_id="AA:BB:CC:DD:EE:FF",
    )


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator."""
    coordinator = MagicMock(spec=MyStromDataUpdateCoordinator)
    coordinator.data = {
        KEY_POWER: 12.5,
        KEY_TEMPERATURE: 23.5,
        KEY_ENERGY: 500,  # Wh
    }
    return coordinator


@pytest.mark.asyncio
async def test_power_sensor_value(mock_coordinator, mock_config_entry):
    """Test power sensor returns correct value."""
    sensor = MyStromPowerSensor(mock_coordinator, mock_config_entry)
    assert sensor.native_value == 12.5


@pytest.mark.asyncio
async def test_power_sensor_none(mock_coordinator, mock_config_entry):
    """Test power sensor returns None when no data."""
    mock_coordinator.data = {}
    sensor = MyStromPowerSensor(mock_coordinator, mock_config_entry)
    assert sensor.native_value is None


@pytest.mark.asyncio
async def test_temperature_sensor_value(mock_coordinator, mock_config_entry):
    """Test temperature sensor returns correct value."""
    sensor = MyStromTemperatureSensor(mock_coordinator, mock_config_entry)
    assert sensor.native_value == 23.5


@pytest.mark.asyncio
async def test_temperature_sensor_none(mock_coordinator, mock_config_entry):
    """Test temperature sensor returns None when no data."""
    mock_coordinator.data = {}
    sensor = MyStromTemperatureSensor(mock_coordinator, mock_config_entry)
    assert sensor.native_value is None


@pytest.mark.asyncio
async def test_energy_sensor_value(mock_coordinator, mock_config_entry):
    """Test energy sensor returns correct value."""
    sensor = MyStromEnergySensor(mock_coordinator, mock_config_entry)
    # Should convert from Wh to kWh
    assert sensor.native_value == 0.5


@pytest.mark.asyncio
async def test_energy_sensor_none(mock_coordinator, mock_config_entry):
    """Test energy sensor returns None when no data."""
    mock_coordinator.data = {}
    sensor = MyStromEnergySensor(mock_coordinator, mock_config_entry)
    assert sensor.native_value is None
