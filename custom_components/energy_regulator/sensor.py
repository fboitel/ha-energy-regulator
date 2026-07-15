from .const import DOMAIN
from .entities.shelly_power_sensor import ShellyPowerSensor

async def async_setup_entry(hass, entry, async_add_entities):

    store = hass.data[DOMAIN][entry.entry_id]["store"]

    async_add_entities([
        ShellyPowerSensor(store),
    ])