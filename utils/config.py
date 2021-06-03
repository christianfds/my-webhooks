import os


class Config():
    DEBUG = os.environ.get('DEBUG', False)
    user_name = os.environ.get('user_name')
    player_uuid = os.environ.get('player_uuid')
