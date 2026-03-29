"""Adds config flow for multical 21."""

import serial
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PORT, CONF_SCAN_INTERVAL, CONF_TIMEOUT
from homeassistant.core import callback

from .const import DEFAULT_BAUDRATE, DEFAULT_SCAN_INTERVAL, DEFAULT_TIMEOUT, DOMAIN


def _test_serial_port(port: str) -> None:
    """Test if the serial port can be opened (blocking, run in executor)."""
    s = serial.Serial(
        port=port,
        baudrate=DEFAULT_BAUDRATE,
        timeout=DEFAULT_TIMEOUT,
    )
    s.close()


class KamstrupFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for multical 21."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Only a single instance of the integration is allowed
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            port = user_input.get(CONF_PORT)
            if port:
                try:
                    await self.hass.async_add_executor_job(_test_serial_port, port)
                    return self.async_create_entry(title=port, data=user_input)
                except serial.SerialException:
                    self._errors["base"] = "port"
            else:
                self._errors["base"] = "port"

            return await self._show_config_form(user_input)

        user_input = {CONF_PORT: ""}
        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return KamstrupOptionsFlowHandler()

    async def _show_config_form(self, user_input):
        """Show the configuration form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PORT, default=user_input[CONF_PORT]): str,
                }
            ),
            errors=self._errors,
        )


class KamstrupOptionsFlowHandler(config_entries.OptionsFlow):
    """Kamstrup config flow options handler."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(
                title=self.config_entry.data.get(CONF_PORT),
                data=user_input,
            )

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
