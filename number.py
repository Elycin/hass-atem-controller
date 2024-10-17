from homeassistant.components.number import NumberEntity
from homeassistant.core import HomeAssistant
from . import ATEM_DEVICE

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the ATEM audio level controls."""
    atem = hass.data[ATEM_DEVICE]
    entities = [ATEMAudioLevelControl(atem, input) for input in atem.inputs]
    async_add_entities(entities, True)

class ATEMAudioLevelControl(NumberEntity):
    """Representation of an ATEM audio level control for an input."""

    def __init__(self, atem, input):
        self._atem = atem
        self._input = input
        self._name = f"ATEM Audio Control {input.long_name}"
        self._state = 0.0

    @property
    def name(self):
        """Return the name of the control."""
        return self._name

    @property
    def value(self):
        """Return the current audio level."""
        return self._state

    @property
    def min_value(self):
        """Return the minimum allowed value (e.g., -100 dB)."""
        return -100.0

    @property
    def max_value(self):
        """Return the maximum allowed value (e.g., 10 dB)."""
        return 10.0

    @property
    def step(self):
        """Return the increment/decrement step size."""
        return 1.0

    async def async_set_value(self, value):
        """Set the audio level for the input."""
        await self._atem.set_audio_input_gain(self._input.input, value)
        self._state = value
        self.async_write_ha_state()
