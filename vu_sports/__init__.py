from flask import Flask
from vu_sports.config import Config
from vu_sports.utils import (
    configure_login_manager,
    db,
    migrate,
    login_manager,
    bootstrap,
    seed_db,
)
from vu_sports.app.routes.root import bp as root_bp
from vu_sports.app.routes.auth import bp as auth_bp
from vu_sports.app.routes.sport import bp as sport_bp
from vu_sports.app.routes.user_request import bp as request_bp
from vu_sports.app.routes.participant import bp as participant_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    configure_login_manager()

    # Register blueprints
    app.register_blueprint(root_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(sport_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(participant_bp)

    # with app.app_context():
    #     seed_db()  # Uncomment this line to seed the database with initial data

    return app
