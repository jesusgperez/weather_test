from config import CACHE_CONFIG
from flask_caching import Cache
from flask import Flask


app = Flask(__name__)
app.cache = Cache(app, config=CACHE_CONFIG)


from routes import weather
app.register_blueprint(weather)
