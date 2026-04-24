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
from vu_sports.app.routes.profile import bp as profile_bp
from vu_sports.app.routes.event import bp as event_bp
from vu_sports.app.routes.team import bp as team_bp
from vu_sports.app.routes.message import bp as message_bp
from vu_sports.app.routes.notification import bp as notification_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db,render_as_batch=True)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    configure_login_manager()

    # Register blueprints
    app.register_blueprint(root_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(sport_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(notification_bp)

    # with app.app_context():
    #     seed_db()  # Uncomment this line to seed the database with initial data

    return app
