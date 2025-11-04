import logging
from logging.handlers import RotatingFileHandler

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    # 🪵 Logging setup
    if not app.debug:
        handler = RotatingFileHandler('app.log', maxBytes=1048576, backupCount=3)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)

    return app
