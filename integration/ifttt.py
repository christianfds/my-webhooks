import requests
from utils.config import config

class Handler():
    def __init__(self, uuid: str):
        self.key = config.get_settings(uuid, 'ifttt')['key']

    def send_event(self, event:str):
        requests.post(f'https://maker.ifttt.com/trigger/{event}/with/key/{self.key}')