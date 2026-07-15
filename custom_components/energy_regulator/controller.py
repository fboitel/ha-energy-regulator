import logging

from homeassistant.helpers.event import async_track_time_interval

from datetime import timedelta
from .const import SHELLY_DEVICE_ID

_LOGGER = logging.getLogger(__name__)


class EnergyRegulatorController:
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry
        self._unsubscribe = None

    async def async_start(self):
        self._unsubscribe = async_track_time_interval(
            self.hass,
            self._tick,
            timedelta(seconds=10),
        )

    async def async_stop(self):
        if self._unsubscribe:
            self._unsubscribe()

    async def _tick(self, now):
        state = self.hass.states.get(SHELLY_DEVICE_ID)
        store = self.hass.data["energy_regulator"][self.entry.entry_id]["store"]
        if state:
            store.shelly_power = float(state.state)

        print("Tick: Mode=%s ManualPower=%s" % (store.automatic_mode, store.manual_power))  
        _LOGGER.info(
            "Mode=%s ManualPower=%s",
            store.automatic_mode,
            store.manual_power,
        )