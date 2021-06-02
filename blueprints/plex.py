import json
from flask import Blueprint, make_response, jsonify, request


plex_app = Blueprint('plex_app', __name__, template_folder='templates')


@plex_app.route('/', methods=['POST'])
def get_webhook_entry():
    received_data = json.loads(request.data.decode('utf-8'))
    print(received_data)

    return make_response(jsonify({
        'teste': 'batata'
    }))
