import logging

from homeassistant.helpers.event import async_track_time_interval

from datetime import timedelta
from .const import BATTERIES, SHELLY_DEVICE_ID, TICK_INTERVAL

from .services.battery import BatteryService
from .services.connector import ConnectorService

_LOGGER = logging.getLogger(__name__)


class EnergyRegulatorController:
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self._unsubscribe_power_setter = None
        self._unsubscribe_mqtt_mode_setter = None
        self.store = self.hass.data["energy_regulator"][self.entry.entry_id]["store"]
        self.battery_service = BatteryService(self.store)
        self.connector_service = ConnectorService(self.hass)

    async def async_start(self):
        self._unsubscribe_power_setter = async_track_time_interval(
            self.hass,
            self._tick_power_setter,
            timedelta(seconds=TICK_INTERVAL),
        )

        self._unsubscribe_mqtt_mode_setter = async_track_time_interval(
            self.hass,
            self._tick_mqtt_mode_setter,
            timedelta(seconds=55),
        )

    async def async_stop(self):
        if self._unsubscribe_power_setter:
            self._unsubscribe_power_setter()
        if self._unsubscribe_mqtt_mode_setter:
            self._unsubscribe_mqtt_mode_setter()

    async def _tick_power_setter(self, now):
        state = self.hass.states.get(SHELLY_DEVICE_ID)
        if state:
            self.store.shelly_power = float(state.state)
            
        self.battery_service.update_power()
        await self.send_battery_powers()
    
    async def _tick_mqtt_mode_setter(self, now):
        await self.set_mqtt_mode()

    async def set_mqtt_mode(self):
        for battery in BATTERIES.keys():
            if battery in self.store.active_batteries:
                entity_id = BATTERIES[battery]
                await self.connector_service.set_mqtt_mode(entity_id)

    async def send_battery_powers(self):
        for battery in BATTERIES.keys():
            if battery in self.store.active_batteries:
                power = self.store.battery_powers[battery]
                entity_id = BATTERIES[battery]
                try:
                    await self.connector_service.send_number(entity_id, power)
                except Exception as e:
                    _LOGGER.error(f"Error sending power to {entity_id}: {e}")
                    print(f"Error sending power to {entity_id}: {e}")
