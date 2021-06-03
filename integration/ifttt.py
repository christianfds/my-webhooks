import requests
from utils.config import Config

class IFTTTHandler():
    def __init__(self):
        self.key = Config.ifttt_key

    def send_event(self, event:str):
        requests.post(f'https://maker.ifttt.com/trigger/{event}/with/key/{self.key}')