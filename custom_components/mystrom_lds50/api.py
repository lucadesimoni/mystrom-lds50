"""API client for MyStrom devices."""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urljoin

import aiohttp

from .const import (
    API_ENDPOINT_OFF,
    API_ENDPOINT_ON,
    API_ENDPOINT_RELAY,
    API_ENDPOINT_REPORT,
    API_ENDPOINT_TOGGLE,
    DEFAULT_TIMEOUT,
    HTTP_STATUS_BAD_REQUEST,
    HTTP_STATUS_NO_CONTENT,
)

_LOGGER = logging.getLogger(__name__)


class MyStromDeviceError(Exception):
    """Base exception for MyStrom device errors."""


class MyStromConnectionError(MyStromDeviceError):
    """Exception raised when connection to device fails."""


class MyStromAPIError(MyStromDeviceError):
    """Exception raised when API returns an error."""


class MyStromAPI:
    """API client for MyStrom devices."""

    def __init__(
        self,
        host: str,
        session: aiohttp.ClientSession,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the MyStrom API client."""
        self.host = host.rstrip("/")
        # MyStrom devices use HTTP, not HTTPS
        self._base_url = f"http://{self.host}"  # nosec
        self._session = session
        self._timeout = aiohttp.ClientTimeout(total=timeout)

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        """
        Make an HTTP request to the device.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            **kwargs: Additional arguments for aiohttp

        Returns:
            Response data as dictionary, or None if empty

        Raises:
            MyStromConnectionError: If connection fails
            MyStromAPIError: If API returns an error

        """
        url = urljoin(self._base_url, endpoint.lstrip("/"))

        try:
            async with self._session.request(
                method,
                url,
                params=params,
                timeout=self._timeout,
                **kwargs,
            ) as response:
                if response.status >= HTTP_STATUS_BAD_REQUEST:
                    error_text = await response.text()
                    msg = f"HTTP {response.status}: {error_text}"
                    raise MyStromAPIError(msg)

                # Some endpoints return empty responses
                if (
                    response.status == HTTP_STATUS_NO_CONTENT
                    or response.content_length == 0
                ):
                    return None

                try:
                    data: dict[str, Any] = await response.json()
                except aiohttp.ContentTypeError:
                    # Some endpoints return plain text
                    if text := await response.text():
                        return {"response": text}
                    return None
                else:  # pylint: disable=no-else-return
                    return data

        except TimeoutError as err:
            msg = f"Timeout connecting to {self.host}: {err}"
            raise MyStromConnectionError(msg) from err
        except aiohttp.ClientError as err:
            msg = f"Error communicating with {self.host}: {err}"
            raise MyStromConnectionError(msg) from err

    async def get_report(self) -> dict[str, Any]:
        """
        Get device status report.

        Returns:
            Device status information

        Raises:
            MyStromConnectionError: If connection fails
            MyStromAPIError: If API returns an error

        """
        if data := await self._request("GET", API_ENDPOINT_REPORT):
            return data
        msg = "Empty response from device"
        raise MyStromAPIError(msg)

    async def set_relay(self, *, state: bool) -> None:
        """
        Set relay state.

        Args:
            state: True to turn on, False to turn off

        Raises:
            MyStromConnectionError: If connection fails
            MyStromAPIError: If API returns an error

        """
        await self._request(
            "GET",
            API_ENDPOINT_RELAY,
            params={"state": 1 if state else 0},
        )

    async def toggle_relay(self) -> dict[str, Any] | None:
        """
        Toggle relay state.

        Returns:
            Updated device status or None

        Raises:
            MyStromConnectionError: If connection fails
            MyStromAPIError: If API returns an error

        """
        return await self._request("GET", API_ENDPOINT_TOGGLE)

    async def turn_on(self) -> None:
        """
        Turn device on.

        Raises:
            MyStromConnectionError: If connection fails
            MyStromAPIError: If API returns an error

        """
        await self._request("GET", API_ENDPOINT_ON)

    async def turn_off(self) -> None:
        """
        Turn device off.

        Raises:
            MyStromConnectionError: If connection fails
            MyStromAPIError: If API returns an error

        """
        await self._request("GET", API_ENDPOINT_OFF)

    async def reboot(self) -> None:
        """
        Reboot the device.

        Raises:
            MyStromConnectionError: If connection fails
            MyStromAPIError: If API returns an error

        """
        await self._request("GET", "/reboot")
