from ..const import MAX_BATTERY_POWER, MIN_BATTERY_POWER

class BatteryService:
    def __init__(self, store):
        self.store = store

    def set_power(self, power: float):
        battery_count = len(self.store.active_batteries)
        if battery_count > 0:
            power_per_battery = max(MIN_BATTERY_POWER, min(MAX_BATTERY_POWER, power / battery_count))
            for battery in self.store.battery_powers.keys():
                if battery in self.store.active_batteries:
                    self.store.battery_powers[battery] = power_per_battery
                else:
                    self.store.battery_powers[battery] = 0.0
        else:
            for battery in self.store.battery_powers.keys():
                self.store.battery_powers[battery] = 0.0
    
    def update_power(self):
        if self.store.automatic_mode:
            self.set_power(self.store.shelly_power)
        else:
            self.set_power(self.store.manual_power)