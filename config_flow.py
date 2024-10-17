import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv
from . import DOMAIN

DATA_SCHEMA = vol.Schema({
    vol.Required("host", default="192.168.1.100"): cv.string
})

class ATEMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ATEM Controller."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            host = user_input["host"]
            try:
                return self.async_create_entry(title="ATEM Controller", data=user_input)
            except Exception:
                errors["base"] = "connection_failed"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
