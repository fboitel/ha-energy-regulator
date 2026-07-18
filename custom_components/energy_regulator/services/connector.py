from ..const import BATTERIES

class ConnectorService:
    def __init__(self, hass):
        self.hass = hass

    async def send_number(self, entity_id: str, value: float):
        number_entity = self.hass.states.get(f"number.{entity_id}")
        if number_entity:
            await self.hass.services.async_call(
                "number",
                "set_value",
                {
                    "entity_id": f"number.{entity_id}",
                    "value": value
                },
                blocking=True,
            )
        else:
            print(f"Number entity {entity_id} not found. Please ensure the number entity exists and is named correctly.")
    
    async def set_mqtt_mode(self, entity_id: str):
        select_entity = self.hass.states.get(f"select.{entity_id}_mqtt_select")
        if select_entity:
            await self.hass.services.async_call(
                "select",
                "select_option",
                {
                    "entity_id": f"select.{entity_id}_mqtt_select",
                    "option": "mqtt_ctrl"
                },
                blocking=True,
            )
        else:
            print(f"Select entity for {entity_id} not found. Please ensure the select entity exists and is named correctly.")