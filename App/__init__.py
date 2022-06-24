from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://2347708a974b4bb8b7c75365b980c08b@o1298044.ingest.sentry.io/6527734",
    integrations=[
        FlaskIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():

    main = Flask(__name__)

    main.config['SECRET_KEY'] = 'secretkey'
    main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    

    from App.models import User

    db.init_app(main)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(main)


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.filter_by(id=user_id).first()

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    main.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    main.register_blueprint(main_blueprint)

    return main

app = create_app()
db.create_all(app=create_app())

