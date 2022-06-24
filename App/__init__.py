# from flask import Flask,render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# app = Flask(__name__)

# app.config.from_object('config')
# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login_page"
# login_manager.login_message_category = "info"

# from App import routes
# from App import models

#models.init_db()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():

    main = Flask(__name__)

    main.config['SECRET_KEY'] = 'secretkey'
    main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    

    from project.models import User

    db.init_app(main)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "info"
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