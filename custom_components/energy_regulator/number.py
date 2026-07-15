
from .entities.power_input import ManualPowerNumber


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        ManualPowerNumber(hass, entry)
    ])