from flask import Flask
from blueprints import plex
from blueprints import sleep_as_android


app = Flask(__name__)
app.config["DEBUG"] = True
app.url_map.strict_slashes = False

# import declared routes
app.register_blueprint(plex.plex_app, url_prefix='/plex')
app.register_blueprint(sleep_as_android.sleep_as_android_app, url_prefix='/sleep_as_android')

app.run()
