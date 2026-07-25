"""Adds config flow for multical 21."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT
from homeassistant.core import callback
import serial
import voluptuous as vol

from .const import DEFAULT_BAUDRATE, DEFAULT_SCAN_INTERVAL, DEFAULT_TIMEOUT, DOMAIN


def _test_serial_port(port: str, baudrate: int, timeout: float) -> None:
    """Test if a serial port can be opened."""
    s = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
    s.close()


class KamstrupFlowHandler(ConfigFlow, domain=DOMAIN):
    """Config flow for multical 21."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await self.hass.async_add_executor_job(
                    _test_serial_port,
                    user_input[CONF_PORT],
                    DEFAULT_BAUDRATE,
                    DEFAULT_TIMEOUT,
                )
            except serial.SerialException:
                errors["base"] = "port"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_PORT], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PORT, default=(user_input or {}).get(CONF_PORT, "")
                    ): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> KamstrupOptionsFlowHandler:
        """Get the options flow for this handler."""
        return KamstrupOptionsFlowHandler()


class KamstrupOptionsFlowHandler(OptionsFlow):
    """Kamstrup config flow options handler."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=86400)),
                    vol.Required(
                        CONF_TIMEOUT,
                        default=self.config_entry.options.get(
                            CONF_TIMEOUT, DEFAULT_TIMEOUT
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=5.0)),
                }
            ),
        )
