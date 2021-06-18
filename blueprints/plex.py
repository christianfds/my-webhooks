import json
from flask import Blueprint, request
from utils.config import config

from integration.integrations import HandleOutputIntegrations


plex_app = Blueprint('plex_app', __name__, template_folder='templates')


class ValidationException(BaseException):
    pass


class PlexHandler():
    def __init__(self, uuid: str, user_name: str, player_uuid: str) -> None:
        self.uuid = uuid
        self.user = config.get_settings(self.uuid, 'plex')
        if self.user:
            raise ValidationException('User without plex configuration')

        if (user_name != self.user['username']):
            raise ValidationException('Doesn\'t run for unspecified users')

        if (player_uuid not in self.user['players']):
            raise ValidationException(f'Doesn\'t run for unspecified player {player_uuid}')

    def handle_event(self, event: str) -> None:
        if event in self.user['trigger_map']:
            HandleOutputIntegrations(self.uuid, self.user)


@plex_app.route('/<uuid>', methods=['POST'])
def webhook_entry(uuid: str):
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

        handler = PlexHandler(uuid, user, player)
        handler.handle_event(event)
    except ValidationException as e:
        pass

    return {'success': True}, 200
