from homeassistant.components.number import NumberEntity
from homeassistant.const import UnitOfPower

class ManualPowerNumber(NumberEntity):

    _attr_name = "Puissance manuelle"
    _attr_native_min_value = -800
    _attr_native_max_value = 800
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfPower.WATT

    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self._attr_native_value = 0

    async def async_set_native_value(self, value):
        self._attr_native_value = value
        self.async_write_ha_state()
        store = self.hass.data["energy_regulator"][self.entry.entry_id]["store"]
        store.manual_power = value