from flask import Flask
from app.config import Config
from app.models.models import db #wipe_user_credentials
from app.routes.auth import auth_bp
from app.routes.pages import pages_bp
from app.routes.weather import weather_bp
from app.routes.news import news
from app.routes.user_comments.submit_comment import subcomment_bp
from app.routes.user_comments.display_comments import displayComms_bp
from app.routes.users import users
import os 

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    root_dir = os.path.join(base_dir, "..")

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=os.path.join(root_dir, "templates"),
        static_folder=os.path.join(root_dir, "static")
    )

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(news)
    app.register_blueprint(users)
    app.register_blueprint(subcomment_bp)
    app.register_blueprint(displayComms_bp)

    with app.app_context():
        # db.drop_all()
         db.create_all()
      #  wipe_user_credentials()
        
    return app