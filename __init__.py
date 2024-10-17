from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from pyatemmax import ATEMMax

DOMAIN = "atem_controller"
ATEM_DEVICE = "atem_device"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ATEM Controller from a config entry."""
    host = entry.data["host"]
    atem = ATEMMax()

    async def connect_atem():
        await atem.connect(host)
        await atem.wait_for_connection()
        hass.data[ATEM_DEVICE] = atem

        # Load related platforms
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "select")
        )
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "sensor")
        )
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "number")
        )

    hass.async_create_task(connect_atem())

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    atem = hass.data.pop(ATEM_DEVICE, None)
    if atem:
        await atem.disconnect()

    # Unload the related platforms
    await hass.config_entries.async_forward_entry_unload(entry, "select")
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    await hass.config_entries.async_forward_entry_unload(entry, "number")

    return True
