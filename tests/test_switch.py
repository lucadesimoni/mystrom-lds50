"""Tests for MyStrom switch platform."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.mystrom_lds50 import async_setup_entry
from custom_components.mystrom_lds50.const import DOMAIN, KEY_POWER, KEY_RELAY
from custom_components.mystrom_lds50.coordinator import MyStromDataUpdateCoordinator
from custom_components.mystrom_lds50.switch import MyStromSwitch


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
def mock_coordinator(mock_api, mock_report_data):
    """Create a mock coordinator."""
    coordinator = MagicMock(spec=MyStromDataUpdateCoordinator)
    coordinator.api = mock_api
    coordinator.data = mock_report_data
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


@pytest.mark.asyncio
async def test_switch_is_on_when_relay_is_on(mock_coordinator, mock_config_entry):
    """Test switch reports on when relay is on."""
    mock_coordinator.data = {KEY_RELAY: 1, KEY_POWER: 12.5}

    switch = MyStromSwitch(mock_coordinator, mock_config_entry)
    assert switch.is_on is True


@pytest.mark.asyncio
async def test_switch_is_off_when_relay_is_off(mock_coordinator, mock_config_entry):
    """Test switch reports off when relay is off."""
    mock_coordinator.data = {KEY_RELAY: 0, KEY_POWER: 0}

    switch = MyStromSwitch(mock_coordinator, mock_config_entry)
    assert switch.is_on is False


@pytest.mark.asyncio
async def test_switch_is_on_by_power(mock_coordinator, mock_config_entry):
    """Test switch reports on based on power consumption."""
    mock_coordinator.data = {KEY_POWER: 12.5}  # No relay key

    switch = MyStromSwitch(mock_coordinator, mock_config_entry)
    assert switch.is_on is True


@pytest.mark.asyncio
async def test_turn_on(mock_coordinator, mock_config_entry):
    """Test turning switch on."""
    switch = MyStromSwitch(mock_coordinator, mock_config_entry)

    await switch.async_turn_on()

    mock_coordinator.api.turn_on.assert_called_once()
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_turn_off(mock_coordinator, mock_config_entry):
    """Test turning switch off."""
    switch = MyStromSwitch(mock_coordinator, mock_config_entry)

    await switch.async_turn_off()

    mock_coordinator.api.turn_off.assert_called_once()
    mock_coordinator.async_request_refresh.assert_called_once()


@pytest.mark.asyncio
async def test_toggle(mock_coordinator, mock_config_entry):
    """Test toggling switch."""
    switch = MyStromSwitch(mock_coordinator, mock_config_entry)

    await switch.async_toggle()

    mock_coordinator.api.toggle_relay.assert_called_once()
    mock_coordinator.async_request_refresh.assert_called_once()
