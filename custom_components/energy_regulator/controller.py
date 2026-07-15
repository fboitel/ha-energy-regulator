import logging

from homeassistant.helpers.event import async_track_time_interval

from datetime import timedelta

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
            timedelta(seconds=15),
        )

    async def async_stop(self):
        if self._unsubscribe:
            self._unsubscribe()

    async def _tick(self, now):
        store = self.hass.data["energy_regulator"][self.entry.entry_id]["store"]
        print("Tick: Mode=%s ManualPower=%s" % (store.automatic_mode, store.manual_power))  
        _LOGGER.info(
            "Mode=%s ManualPower=%s",
            store.automatic_mode,
            store.manual_power,
        )