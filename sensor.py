from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from . import ATEM_DEVICE

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the ATEM audio level sensors."""
    atem = hass.data[ATEM_DEVICE]
    entities = [ATEMAudioLevelSensor(atem, input) for input in atem.inputs]
    async_add_entities(entities, True)

class ATEMAudioLevelSensor(SensorEntity):
    """Representation of an ATEM input audio level."""

    def __init__(self, atem, input):
        self._atem = atem
        self._input = input
        self._name = f"ATEM Audio Level {input.long_name}"
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the current audio level for this input."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "dB"

    async def async_update(self):
        """Fetch the latest audio level from the ATEM."""
        audio_levels = self._atem.audio_levels
        if self._input.input in audio_levels:
            self._state = audio_levels[self._input.input].dbfs
