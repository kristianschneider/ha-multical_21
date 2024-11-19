"""
Custom integration to integrate multical_21 with Home Assistant.

For more details about this integration, please refer to
https://github.com/kristianschneider/ha-multical_21/
"""
from datetime import timedelta
import logging
from typing import Any, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import serial

from .const import (
    DEFAULT_BAUDRATE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TIMEOUT,
    DOMAIN,
    NAME,
    PLATFORMS,
    VERSION,
)
from .pykamstrup.kamstrup import Kamstrup

_LOGGER = logging.getLogger(__name__)


async def async_setup(_hass: HomeAssistant, _config: Config) -> bool:
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    port = entry.data.get(CONF_PORT)
    scan_interval_seconds = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    scan_interval = timedelta(seconds=scan_interval_seconds)
    timeout_seconds = entry.options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)

    _LOGGER.debug(
        "Set up entry, with scan_interval of %s seconds and timeout of %s seconds",
        scan_interval_seconds,
        timeout_seconds,
    )

    try:
        client = Kamstrup(port, DEFAULT_BAUDRATE, timeout_seconds)
    except Exception as exception:
        _LOGGER.error("Can't establish a connection with %s", port)
        raise ConfigEntryNotReady() from exception

    device_info = DeviceInfo(
        entry_type=DeviceEntryType.SERVICE,
        identifiers={(DOMAIN, port)},
        manufacturer=NAME,
        name=NAME,
        model=VERSION,
    )

    coordinator = KamstrupUpdateCoordinator(
        hass=hass, client=client, scan_interval=scan_interval, device_info=device_info
    )

    hass.data[DOMAIN][entry.entry_id] = coordinator


    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await coordinator.async_config_entry_first_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_close()

    return unload_ok


async def async_reload_entry(hass, entry):
    await hass.config_entries.async_reload(entry.entry_id)


class KamstrupUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Kamstrup serial reader."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: Kamstrup,
        scan_interval: int,
        device_info: DeviceInfo,
    ) -> None:
        """Initialize."""
        self.kamstrup = client
        self.device_info = device_info

        self._commands: List[int] = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=scan_interval)

    def register_command(self, command: int) -> None:
        """Add a command to the commands list."""
        _LOGGER.debug("Register command %s", command)
        self._commands.append(command)

    def unregister_command(self, command: int) -> None:
        """Remove a command from the commands list."""
        _LOGGER.debug("Unregister command %s", command)
        self._commands.remove(command)
    async def async_close(self) -> None:
        """Close resources."""
        _LOGGER.debug("Closing Kamstrup connection")
        self.kamstrup = None

    async def _async_update_data(self) -> dict[int, Any]:
        """Update data via library."""
        _LOGGER.debug("Start update")

        data = {}

        try:
            values = self.kamstrup.get_values(self._commands)
        except serial.SerialException as exception:
            _LOGGER.error(
                "Device disconnected or multiple access on port? \nException: %e",
                exception,
            )
        except Exception as exception:
            _LOGGER.error(
                "Error reading multiple %s \nException: %s", self._commands, exception
            )
            raise UpdateFailed() from exception

        failed_counter = len(self._commands) - len(values)

        for command in self._commands:
            if command in values:
                value, unit = values[command]
                data[command] = {"value": value, "unit": unit}
                _LOGGER.debug(
                    "New value for sensor %s, value: %s %s", command, value, unit
                )

        if failed_counter == len(data):
            _LOGGER.error(
                "Finished update, No readings from the meter. Please check the IR connection"
            )
        else:
            _LOGGER.debug(
                "Finished update, %s out of %s readings failed",
                failed_counter,
                len(data),
            )

        return data
