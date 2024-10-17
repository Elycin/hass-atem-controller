from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from . import ATEM_DEVICE

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the ATEM select entity from a config entry."""
    atem = hass.data[ATEM_DEVICE]
    async_add_entities([ATEMProgramSelect(atem)], True)

class ATEMProgramSelect(SelectEntity):
    """Representation of an ATEM input selector."""

    def __init__(self, atem):
        self._atem = atem
        self._name = "ATEM Program Selector"
        self._current_input = None

    @property
    def name(self):
        """Return the name of the entity."""
        return self._name

    @property
    def options(self):
        """Return a list of available input options."""
        return [input.long_name for input in self._atem.inputs]

    @property
    def current_option(self):
        """Return the currently selected input."""
        return self._current_input

    async def async_select_option(self, option):
        """Set the ATEM program to the selected input."""
        input_source = next((input for input in self._atem.inputs if input.long_name == option), None)
        if input_source:
            await self._atem.set_program_input(input_source.input)
            self._current_input = option
            self.async_write_ha_state()
