from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, static_url_path="", static_folder="static")
app.config.from_object(Config)

db = SQLAlchemy(app)
login = LoginManager(app)

from app import routes, models