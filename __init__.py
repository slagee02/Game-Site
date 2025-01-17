from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy
from config import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
db = SQLAlchemy()
bcrypt = Bcrypt(app)

proxied = FlaskBehindProxy(app)