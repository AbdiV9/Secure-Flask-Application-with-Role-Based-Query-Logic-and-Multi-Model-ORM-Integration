from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy() # db is defined here

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app) #  db is initialized/linked to the app here

    from .routes import main
    app.register_blueprint(main)

    return app
