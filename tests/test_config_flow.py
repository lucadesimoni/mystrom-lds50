"""Tests for MyStrom config flow."""

from unittest.mock import AsyncMock, patch

import pytest

from custom_components.mystrom_lds50.config_flow import CannotConnect, ConfigFlow
from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant


@pytest.fixture
def mock_api_success():
    """Mock successful API response."""
    with patch(
        "custom_components.mystrom_lds50.config_flow.MyStromAPI"
    ) as mock_api:
        mock_instance = AsyncMock()
        mock_instance.get_report.return_value = {
            "power": 12.5,
            "relay": 1,
            "mac": "AA:BB:CC:DD:EE:FF",
            "type": "Switch",
        }
        mock_instance.close = AsyncMock()
        mock_api.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_api_connection_error():
    """Mock API connection error."""
    with patch(
        "custom_components.mystrom_lds50.config_flow.MyStromAPI"
    ) as mock_api:
        mock_instance = AsyncMock()
        mock_instance.get_report.side_effect = Exception("Connection error")
        mock_instance.close = AsyncMock()
        mock_api.return_value = mock_instance
        yield mock_instance


@pytest.mark.asyncio
async def test_flow_user_success(hass: HomeAssistant, mock_api_success):
    """Test successful user flow."""
    flow = ConfigFlow()
    flow.hass = hass
    flow._async_abort_entries_match = AsyncMock()

    result = await flow.async_step_user(
        user_input={
            "host": "192.168.1.100",
            "name": "MyStrom Switch",
            "device_type": "switch",
        }
    )

    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["title"] == "MyStrom Switch"
    assert result["data"]["host"] == "192.168.1.100"


@pytest.mark.asyncio
async def test_flow_user_connection_error(
    hass: HomeAssistant, mock_api_connection_error
):
    """Test user flow with connection error."""
    flow = ConfigFlow()
    flow.hass = hass
    flow._async_abort_entries_match = AsyncMock()

    result = await flow.async_step_user(
        user_input={
            "host": "192.168.1.100",
            "name": "MyStrom Switch",
            "device_type": "switch",
        }
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"]["base"] == "cannot_connect"


@pytest.mark.asyncio
async def test_flow_user_no_input(hass: HomeAssistant):
    """Test user flow with no input."""
    flow = ConfigFlow()
    flow.hass = hass

    result = await flow.async_step_user(user_input=None)

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert "data_schema" in result

