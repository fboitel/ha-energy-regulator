from ..const import MAX_BATTERY_POWER, MIN_BATTERY_POWER, DEAD_BAND

class BatteryService:
    # Use a smart algorithm to order the battery charge/discharge based on the current grid power.
    def __init__(self, store):
        self.store = store
        self.battery_command = 0
        self.filtered_grid_power = 0

    def compute_power(self, power: float):
        self.filtered_grid_power = (self.filtered_grid_power * 0.8) + (power * 0.2)

        if abs(self.filtered_grid_power) < DEAD_BAND:
            self.store.overall_battery_command = self.battery_command
            self.store.filtered_grid_power = self.filtered_grid_power
            self.store.grid_power = power
            return
        
        self.battery_command = 0.7 * self.battery_command + 0.3 * self.filtered_grid_power 

        if (self.battery_command % 1) < 0.5:
            self.battery_command += 0.1
        else:
            self.battery_command -= 0.1

        self.store.overall_battery_command = self.battery_command
        self.store.filtered_grid_power = self.filtered_grid_power
        self.store.grid_power = power
        

    def set_power(self):
        battery_count = len(self.store.active_batteries)
        if battery_count > 0:
            power_per_battery = max(MIN_BATTERY_POWER, min(MAX_BATTERY_POWER, self.battery_command / battery_count))
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
            self.compute_power(self.store.shelly_power)
        else:
            self.compute_power(self.store.manual_power)
    
        self.set_power()

        