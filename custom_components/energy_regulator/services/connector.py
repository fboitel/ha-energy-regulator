from ..const import BATTERIES

class ConnectorService:
    def __init__(self, hass):
        self.hass = hass

    async def send_number(self, entity_id: str, value: float):
        number_entity = self.hass.states.get(entity_id)
        if number_entity:
            await self.hass.services.async_call(
                "number",
                "set_value",
                {
                    "entity_id": f"{entity_id}",
                    "value": value
                },
                blocking=True,
            )
    
    async def set_mqtt_mode(self, entity_id: str):
        await self.hass.services.async_call(
            "select",
            "select_option",
            {
                "entity_id": f"{entity_id}_mqtt_select",
                "option": "mqtt_ctrl"
            },
            blocking=True,
        )