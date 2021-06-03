import json
from flask import Blueprint, request
from utils.config import Config

from integration.ifttt import IFTTTHandler


sleep_as_android_app = Blueprint('sleep_as_android_app', __name__, template_folder='templates')


class ValidationException(BaseException):
    pass


class SleepAsAndroidHandler():
    def __init__(self) -> None:
        self.event_handler = IFTTTHandler()

    def _lights_low_dim(self):
        print('Ligando as luzes com brilho baixo')
        self.event_handler.send_event('lights_low_dim')

    def _lights_on(self):
        print('Ligando as luzes')
        self.event_handler.send_event('lights_on')

    def _lights_off(self):
        print('Desligando as luzes')
        self.event_handler.send_event('lights_off')

    def handle_event(self, event: str) -> None:
        EVENT_MAP = {
            'sleep_tracking_started': self._lights_off,
            # 'sleep_tracking_stopped': self._lights_on,
            'alarm_alert_start': self._lights_on,
            'alarm_alert_dismiss': self._lights_low_dim,
            'alarm_snooze_clicked': self._lights_off,
            'alarm_snooze_canceled': self._lights_low_dim,
        }

        if event in EVENT_MAP:
            EVENT_MAP[event]()


@sleep_as_android_app.route('/', methods=['POST'])
def get_webhook_entry():
    payload = request.get_json()
    try:
        handler = SleepAsAndroidHandler()
        handler.handle_event(payload.get('event'))
    except ValidationException:
        pass

    return {'success': True}, 200
