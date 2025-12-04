"""Constants for the MyStrom LDS50 integration."""

DOMAIN = "mystrom_lds50"

# Device types
DEVICE_TYPE_SWITCH = "switch"
DEVICE_TYPE_ZERO = "zero"
DEVICE_TYPE_BULB = "bulb"
DEVICE_TYPE_BUTTON = "button"

# Configuration keys
CONF_HOST = "host"
CONF_MAC = "mac"
CONF_NAME = "name"
CONF_DEVICE_TYPE = "device_type"
CONF_TOKEN = "token"  # nosec B105

# Default values
DEFAULT_TIMEOUT = 10
DEFAULT_SCAN_INTERVAL = 30

# HTTP status codes
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_NO_CONTENT = 204

# Energy conversion
ENERGY_WH_TO_KWH_THRESHOLD = 1000

# API endpoints
API_ENDPOINT_REPORT = "/report"
API_ENDPOINT_RELAY = "/relay"
API_ENDPOINT_TOGGLE = "/toggle"
API_ENDPOINT_ON = "/on"
API_ENDPOINT_OFF = "/off"

# Device status keys
KEY_POWER = "power"
KEY_RELAY = "relay"
KEY_TEMPERATURE = "temperature"
KEY_ENERGY = "W"
KEY_WS = "ws"  # WiFi signal strength

# Service names
SERVICE_SET_RELAY_STATE = "set_relay_state"
SERVICE_TOGGLE_RELAY = "toggle_relay"
SERVICE_REBOOT = "reboot"
SERVICE_SET_WLAN = "set_wlan"

# Attributes
ATTR_POWER = "power"
ATTR_TEMPERATURE = "temperature"
ATTR_ENERGY = "energy"
ATTR_WIFI_SIGNAL = "wifi_signal"
ATTR_FIRMWARE = "firmware"
ATTR_MAC = "mac"
ATTR_HOST = "host"
ATTR_DEVICE_TYPE = "device_type"

# Errors
ERROR_CANNOT_CONNECT = "cannot_connect"
ERROR_INVALID_AUTH = "invalid_auth"
ERROR_UNKNOWN = "unknown"
