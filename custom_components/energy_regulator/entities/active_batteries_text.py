from homeassistant.components.text import TextEntity

from ..const import BATTERIES

class ActiveBatteriesText(TextEntity):

    _attr_name = "Batteries actives"

    def __init__(self, store):
        self.store = store
        self._attr_native_value = ",".join([key for key in BATTERIES.keys()])

    def text_to_list(self, text):
        return [key.strip() for key in text.split(",") if key.strip() in BATTERIES.keys()]


    async def async_set_value(self, value):
        self._attr_native_value = value
        self.async_write_ha_state()
        self.store.active_batteries = self.text_to_list(value)