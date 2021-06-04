import json
from flask import Blueprint, request
from utils.config import Config

from integration.ifttt import IFTTTHandler


plex_app = Blueprint('plex_app', __name__, template_folder='templates')


class ValidationException(BaseException):
    pass


class PlexHandler():
    def __init__(self, user_name: str, player_uuid: str) -> None:
        if (user_name != Config.user_name):
            raise ValidationException('Doesn\'t run for unspecified users')

        if (player_uuid != Config.player_uuid):
            raise ValidationException('Doesn\'t run for unspecified players')

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
            'media.play': self._lights_off,
            'media.pause': self._lights_low_dim,
            'media.resume': self._lights_off,
            'media.stop': self._lights_on
        }

        if event in EVENT_MAP:
            EVENT_MAP[event]()


@plex_app.route('/', methods=['POST'])
def webhook_entry():
    payload = request.form.to_dict().get('payload')
    if not payload:
        return {'success': False}, 400

    payload = json.loads(payload)
    if not payload.get('user', False):
        return {'success': False}, 400

    try:
        user = payload.get('Account', {}).get('title')
        player = payload.get('Player', {}).get('uuid')
        event = payload.get('event')

        handler = PlexHandler(user, player)
        handler.handle_event(event)
    except ValidationException as e:
        pass

    return {'success': True}, 200
