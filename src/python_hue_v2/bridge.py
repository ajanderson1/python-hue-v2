import json

import requests
import urllib3
from typing import List


class Bridge:
    def __init__(self, ip_address: str, hue_application_key: str):
        self.ip_address = ip_address
        self.hue_application_key = hue_application_key
        self.hue_application_key_str = 'hue-application-key'
        # url
        self.base_url = f'https://{self.ip_address}/clip/v2/resource'

        self._light_category = 'light'
        self._scene_category = 'scene'
        self._room_category = 'room'
        self._zone_category = 'zone'
        self._bridge_home_category = 'bridge_home'
        self._grouped_light_category = 'grouped_light'
        self._device_category = 'device'

        self.device_list: list = []
        # requests.Request.
        urllib3.disable_warnings()

    @staticmethod
    def _get_response_error(r_json: dict):
        return r_json['errors']

    @staticmethod
    def _get_response_data(r_json: dict) -> list:
        return r_json['data']

    @staticmethod
    def _convert_to_data(res: dict) -> List[dict]:
        if res['errors']:
            raise ConnectionError(res['errors'])
        else:
            return res['data']

    def _get_by_id(self, category: str, item_id: str) -> List[dict]:
        url = f'{self.base_url}/{category}/{item_id}'
        res = requests.get(url, headers={self.hue_application_key_str: self.hue_application_key}, verify=False).json()
        return self._convert_to_data(res)

    def _get(self, category: str) -> List[dict]:
        url = f'{self.base_url}/{category}'
        res = requests.get(url, headers={self.hue_application_key_str: self.hue_application_key}, verify=False).json()
        return self._convert_to_data(res)

    def _put_by_id(self, category: str, item_id: str, properties: dict):
        url = f'{self.base_url}/{category}/{item_id}'
        res = requests.put(url, data=json.dumps(properties),
                           headers={self.hue_application_key_str: self.hue_application_key},
                           verify=False).json()
        return self._convert_to_data(res)

    def raw_get_light(self, light_id: str) -> List[dict]:
        return self._get_by_id(self._light_category, light_id)

    def raw_get_lights(self) -> List[dict]:
        """
        Get all lights info in bridge
        :return:
        """
        return self._get(self._light_category)

    @property
    def lights(self) -> List[dict]:
        return self.raw_get_lights()

    def raw_get_scenes(self) -> List[dict]:
        return self._get(self._scene_category)

    def raw_get_scene(self, scene_id) -> List[dict]:
        return self._get_by_id(self._scene_category, scene_id)

    def raw_get_rooms(self) -> List[dict]:
        return self._get(self._room_category)

    def raw_get_room(self, room_id: str) -> List[dict]:
        return self._get_by_id(self._room_category, room_id)

    def raw_get_zones(self) -> List[dict]:
        return self._get(self._zone_category)

    def raw_get_zone(self, zone_id: str) -> List[dict]:
        return self._get_by_id(self._zone_category, zone_id)

    def raw_get_devices(self):
        return self._get(self._device_category)

    def raw_get_device(self, device_id: str):
        return self._get_by_id(self._device_category, device_id)

    def raw_set_light(self, light_id_v2, light_property, key_value: dict):
        data = {light_property: key_value}
        return self._put_by_id(self._light_category, light_id_v2, data)


if __name__ == '__main__':
    hue = Bridge('ecb5fa8549cd.local', '7K-IbBzEV3wZoXkTlSh6HyLTALLFsYrxCjIcW1o9')
    # hue.get_device()
    print(hue.raw_get_lights())
    print(hue.raw_set_light('de2bf1a8-7153-4f8d-970e-af32297452e8', 'on', {'on': False}))
    print(hue.raw_get_scenes())
    # print(hue.lights)
    # print(hue.raw_get_devices())
