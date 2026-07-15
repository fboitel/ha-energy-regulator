from homeassistant.const import UnitOfPower
from homeassistant.components.sensor import SensorEntity

class ShellyPowerSensor(SensorEntity):

    _attr_name = "Puissance Shelly"
    _attr_native_unit_of_measurement = UnitOfPower.WATT

    def __init__(self, store):
        self.store = store

    @property
    def native_value(self):
        return self.store.shelly_power