from ..const import BATTERIES

class ConnectorService:
    def __init__(self, hass):
        self.hass = hass

    def send_number(self, entity_id: str, value: float):
        number_entity = self.hass.states.get(entity_id)
        if number_entity:
            self.hass.services.call(
                "number",
                "set_value",
                {
                    "entity_id": f"number.{entity_id}",
                    "value": value
                },
            )
    
    def set_mqtt_mode(self, entity_id: str):
        self.hass.services.call(
            "select",
            "select_option",
            {
                "entity_id": f"select.{entity_id}_mqtt_select",
                "option": "mqtt_ctrl"
            },
        )