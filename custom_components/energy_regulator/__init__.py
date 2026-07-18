from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .controller import EnergyRegulatorController
from .const import DOMAIN
from .store import Store

PLATFORMS = ["switch", "number", "sensor", "text"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up Energy Regulator."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    hass.data[DOMAIN].setdefault(entry.entry_id, {})
    hass.data[DOMAIN][entry.entry_id]["store"] = Store()
    controller = EnergyRegulatorController(hass, entry)
    hass.data[DOMAIN][entry.entry_id]["controller"] = controller

    await controller.async_start()

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):
    """Unload."""
    controller = hass.data[DOMAIN][entry.entry_id]["controller"]
    await controller.async_stop()
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok