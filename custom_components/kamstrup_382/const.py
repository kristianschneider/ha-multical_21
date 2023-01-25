"""Constants for Kamstrup 382."""

from typing import Final

# Base component constants
NAME: Final = "Kamstrup 382"
DOMAIN: Final = "kamstrup_382"
VERSION: Final = "2.1.0"
MODEL: Final = "382"
MANUFACTURER: Final = "Kamstrup"
ATTRIBUTION: Final = "Data provided by Kamstrup 382 meter"

# Defaults
DEFAULT_NAME: Final = NAME
DEFAULT_BAUDRATE: Final = 9600
DEFAULT_SCAN_INTERVAL: Final = 60
DEFAULT_TIMEOUT: Final = 1.0

# Platforms
SENSOR: Final = "sensor"
PLATFORMS: Final = [SENSOR]
