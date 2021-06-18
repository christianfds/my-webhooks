import os
import json
import typing


class Config():

    def __init__(self) -> None:
        self.json_conf = None
        with open('config/settings.json') as config_file:
            self.json_conf = json.load(config_file)

        self.DEBUG = self.json_conf['debug']
        self.users = self.json_conf.get('users')
        
    def get_settings(self, uuid: str, config: str) -> typing.Dict:
        return self.users.get(uuid, {}).get(config, {})

config = Config()