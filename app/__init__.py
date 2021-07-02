from flask import Flask
from app.views.views import bp as bp_anime 


def create_app(app):
    app = Flask(__name__)

    app.register_blueprint(bp_anime)
    
    return app