import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
# bind LoginManager to this app
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_global_app():
  # Create a new Flask app instance
  app = Flask(__name__,instance_relative_config=True)

  # Configure 
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev-only-fallback')
  db_path=os.path.join(app.instance_path, 'playdate.db')
  app.config["SQLALCHEMY_DATABASE_URI"]= f"sqlite:///{db_path}"
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False #to enable or disable tracking modifications of objects. 

  # Ensure instance folder exists
  os.makedirs(app.instance_path,exist_ok=True)

  # Init extensions
  db.init_app(app)    # bind SQLAlchemy to this app
  login_manager.init_app(app)  # bind LoginManager to this app
  bcrypt.init_app(app)  # bind Bcrypt to this app

  # Import models *after* db init to avoid circular import
  from flaskplaydate import models

  #Configure LoginManager behavior
  login_manager.login_view = 'main.login'
  login_manager.login_message_category = 'info'

  # Import routes *after* app is ready
  from flaskplaydate import routes
  from flaskplaydate.routes import main
  app.register_blueprint(main)

  print("App root:", app.root_path)
  print("Instance path:", app.instance_path)
  print("DB absolute:", db_path)

  return app

# Global pattern: create app instance at import
#app = create_global_app()


