from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .entities.mode_switch import EnergyModeSwitch


async def async_setup_entry(hass, entry, async_add_entities):

    async_add_entities([
        EnergyModeSwitch(hass, entry)
    ])

