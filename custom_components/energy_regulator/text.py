from .entities.active_batteries_text import ActiveBatteriesText

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):

    store = hass.data[DOMAIN][entry.entry_id]["store"]

    async_add_entities([
        ActiveBatteriesText(store),
    ])