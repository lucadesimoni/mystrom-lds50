"""Tests for MyStrom API client."""

from unittest.mock import AsyncMock

import pytest

from custom_components.mystrom_lds50.api import (
    MyStromAPI,
    MyStromAPIError,
)


@pytest.mark.asyncio
async def test_api_init():
    """Test API client initialization."""
    mock_session = AsyncMock()
    api = MyStromAPI("192.168.1.100", session=mock_session)
    assert api.host == "192.168.1.100"
    assert api._base_url == "http://192.168.1.100"


@pytest.mark.asyncio
async def test_get_report_success():
    """Test successful device report retrieval."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value={
            "power": 12.5,
            "relay": 1,
            "temperature": 23.5,
            "mac": "AA:BB:CC:DD:EE:FF",
        }
    )

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    api = MyStromAPI("192.168.1.100", session=mock_session)

    data = await api.get_report()

    assert data["power"] == 12.5
    assert data["relay"] == 1
    assert data["temperature"] == 23.5


@pytest.mark.asyncio
async def test_set_relay():
    """Test setting relay state."""
    mock_response = AsyncMock()
    mock_response.status = 204
    mock_response.content_length = 0

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    api = MyStromAPI("192.168.1.100", session=mock_session)

    await api.set_relay(True)
    await api.set_relay(False)


@pytest.mark.asyncio
async def test_toggle_relay():
    """Test toggling relay."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={"relay": 1})

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    api = MyStromAPI("192.168.1.100", session=mock_session)

    data = await api.toggle_relay()
    assert data["relay"] == 1


@pytest.mark.asyncio
async def test_turn_on_off():
    """Test turning device on and off."""
    mock_response = AsyncMock()
    mock_response.status = 204
    mock_response.content_length = 0

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    api = MyStromAPI("192.168.1.100", session=mock_session)

    await api.turn_on()
    await api.turn_off()


@pytest.mark.asyncio
async def test_reboot():
    """Test rebooting device."""
    mock_response = AsyncMock()
    mock_response.status = 204
    mock_response.content_length = 0

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    api = MyStromAPI("192.168.1.100", session=mock_session)

    await api.reboot()


@pytest.mark.asyncio
async def test_api_error_handling():
    """Test API error handling."""
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.text = AsyncMock(return_value="Not Found")

    mock_session = AsyncMock()
    mock_session.request = AsyncMock(return_value=mock_response)
    mock_session.__aenter__ = AsyncMock(return_value=mock_response)
    mock_session.__aexit__ = AsyncMock(return_value=None)

    api = MyStromAPI("192.168.1.100", session=mock_session)

    with pytest.raises(MyStromAPIError):
        await api.get_report()


@pytest.mark.asyncio
async def test_reuse_session():
    """Test reusing an existing session."""
    mock_session = AsyncMock()

    api = MyStromAPI("192.168.1.100", session=mock_session)
    assert api._session is mock_session
