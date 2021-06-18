from flask import Blueprint, request
from utils.config import config

from integration.integrations import HandleOutputIntegrations


sleep_as_android_app = Blueprint('sleep_as_android_app', __name__, template_folder='templates')


class ValidationException(BaseException):
    pass


class SleepAsAndroidHandler():
    def __init__(self, uuid: str) -> None:
        self.uuid = uuid
        self.user = config.get_settings(self.uuid, 'sleep_as_android')

    def handle_event(self, event: str) -> None:
        if event in self.user['trigger_map']:
            HandleOutputIntegrations.send_event(self.uuid, self.user['trigger_map'][event])


@sleep_as_android_app.route('/<uuid>', methods=['POST'])
def get_webhook_entry(uuid: str):
    payload = request.get_json()
    try:
        handler = SleepAsAndroidHandler(uuid)
        handler.handle_event(payload.get('event'))
    except ValidationException:
        pass

    return {'success': True}, 200
