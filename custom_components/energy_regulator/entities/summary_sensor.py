from homeassistant.const import UnitOfPower
from homeassistant.components.sensor import SensorEntity

class SummarySensor(SensorEntity):

    _attr_name = "Aperçu"

    def __init__(self, store):
        self.store = store

    def battery_summary(self):
        return "\n".join(
            [
                "%s:%.2f" % (key, power)
                for key, power in self.store.battery_powers.items()
            ]
        )

    @property
    def native_value(self):
        return "Auto=%s Manuel=%.2f Shelly=%.2f %s" % (
            self.store.automatic_mode,
            self.store.manual_power,
            self.store.shelly_power,
            self.battery_summary(),
        )