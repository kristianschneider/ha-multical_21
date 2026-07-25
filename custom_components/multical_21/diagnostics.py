"""Diagnostics support for multical_21."""

from homeassistant.core import HomeAssistant

from . import KamstrupConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, config_entry: KamstrupConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""
    coordinator = config_entry.runtime_data

    return {
        "config_entry": config_entry.as_dict(),
        "data": coordinator.data,
    }
