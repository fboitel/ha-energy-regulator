from homeassistant.components.switch import SwitchEntity

from ..const import DOMAIN

class EnergyModeSwitch(SwitchEntity):

    _attr_name = "Régulation automatique"
    _attr_is_on = True

    def __init__(self, hass, entry):
        self._attr_is_on = True
        self.hass = hass
        self.entry = entry

    async def async_turn_on(self, **kwargs):
        self._attr_is_on = True
        self.async_write_ha_state()
        store = self.hass.data[DOMAIN][self.entry.entry_id]["store"]
        store.automatic_mode = True

    async def async_turn_off(self, **kwargs):
        self._attr_is_on = False
        self.async_write_ha_state()
        store = self.hass.data[DOMAIN][self.entry.entry_id]["store"]
        store.automatic_mode = False