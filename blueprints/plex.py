import json
from flask import Blueprint, make_response, jsonify, request


plex_app = Blueprint('plex_app', __name__, template_folder='templates')


@plex_app.route('/', methods=['POST'])
def get_webhook_entry():
    payload = request.form.to_dict().get('payload')
    if payload:
        payload = json.loads(payload)

    print(payload)

    return make_response(jsonify({
        'teste': 'batata'
    }))
