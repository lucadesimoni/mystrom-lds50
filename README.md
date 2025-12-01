# MyStrom LDS50 Integration for Home Assistant

A lightweight, modern Home Assistant integration for MyStrom devices (Switch, Zero, Bulb, Button) with full REST API support.

## Features

- ✅ **Lightweight & Fast**: Minimal dependencies, efficient polling
- ✅ **Full API Support**: All MyStrom Switch and Zero REST API commands
- ✅ **Modern Architecture**: Uses Home Assistant coordinators and best practices
- ✅ **Device Support**: MyStrom Switch, Zero, Bulb, and Button
- ✅ **Sensors**: Power consumption, temperature, and energy monitoring
- ✅ **Services**: Advanced control via Home Assistant services

## Supported Devices

- MyStrom Switch
- MyStrom Zero
- MyStrom Bulb
- MyStrom Button

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots menu and select "Custom repositories"
4. Add this repository URL
5. Search for "MyStrom LDS50" and install

### Manual Installation

1. Copy the `custom_components/mystrom_lds50` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "MyStrom LDS50"

## Configuration

1. Go to Settings → Devices & Services → Add Integration
2. Search for "MyStrom LDS50"
3. Enter your device IP address (and optional MAC address)
4. The integration will automatically detect your device type

## Available Entities

### Switch
- Main relay control

### Sensors
- **Power**: Current power consumption (W)
- **Temperature**: Device temperature (if supported)
- **Energy**: Total energy consumption (kWh, if supported)

## Services

### `mystrom_lds50.set_relay_state`
Set the relay state directly.

**Service Data:**
```yaml
entity_id: switch.mystrom_device
state: true  # or false
```

### `mystrom_lds50.toggle_relay`
Toggle the relay state.

**Service Data:**
```yaml
entity_id: switch.mystrom_device
```

### `mystrom_lds50.reboot`
Reboot the device.

**Service Data:**
```yaml
entity_id: switch.mystrom_device
```

## REST API Endpoints Supported

The integration supports all standard MyStrom REST API endpoints:

- `GET /report` - Get device status
- `GET /relay?state=0|1` - Set relay state
- `GET /toggle` - Toggle relay
- `GET /on` - Turn on
- `GET /off` - Turn off
- `GET /reboot` - Reboot device

## Requirements

- Home Assistant 2025.8.0 or later
- Python 3.11+

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Lint code
ruff check custom_components/mystrom_lds50/
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
