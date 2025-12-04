"""Pytest configuration and fixtures."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientSession

from custom_components.mystrom_lds50.api import MyStromAPI


@pytest.fixture
def mock_api():
    """Create a mock MyStrom API."""
    api = MagicMock(spec=MyStromAPI)
    api.host = "192.168.1.100"
    api.get_report = AsyncMock()
    api.set_relay = AsyncMock()
    api.toggle_relay = AsyncMock()
    api.turn_on = AsyncMock()
    api.turn_off = AsyncMock()
    api.reboot = AsyncMock()
    return api


@pytest.fixture
def mock_report_data():
    """Mock device report data."""
    return {
        "power": 12.5,
        "relay": 1,
        "temperature": 23.5,
        "mac": "AA:BB:CC:DD:EE:FF",
        "type": "Switch",
        "W": 0.5,  # Energy in Wh
        "ws": -50,  # WiFi signal strength
    }


@pytest.fixture
def mock_report_data_zero():
    """Mock MyStrom Zero device report data."""
    return {
        "power": 0.0,
        "relay": 0,
        "mac": "AA:BB:CC:DD:EE:00",
        "type": "Zero",
    }


@pytest.fixture
def mock_session():
    """Create a mock aiohttp session."""
    return AsyncMock(spec=ClientSession)
