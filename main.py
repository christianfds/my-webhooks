from flask import Flask
from blueprints import plex


app = Flask(__name__)
app.config["DEBUG"] = True
app.url_map.strict_slashes = False

# import declared routes
app.register_blueprint(plex.plex_app, url_prefix='/plex')

app.run()
