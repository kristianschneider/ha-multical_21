"""Constants for multical 21."""

from typing import Final

# Base component constants
NAME: Final = "multical 21"
DOMAIN: Final = "multical_21"
VERSION: Final = "2.1.0"
MODEL: Final = "382"
MANUFACTURER: Final = "Kamstrup"
ATTRIBUTION: Final = "Data provided by multical 21 meter"

# Defaults
DEFAULT_NAME: Final = NAME
DEFAULT_BAUDRATE: Final = 1200
DEFAULT_SCAN_INTERVAL: Final = 60
DEFAULT_TIMEOUT: Final = 1.0

# Platforms
SENSOR: Final = "sensor"
PLATFORMS: Final = [SENSOR]
