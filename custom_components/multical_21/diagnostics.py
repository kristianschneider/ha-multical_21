"""Diagnostics support for multical_21."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import DOMAIN, KamstrupUpdateCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    coordinator: KamstrupUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    return {
        "config_entry": config_entry.as_dict(),
        "data": coordinator.data,
    }
