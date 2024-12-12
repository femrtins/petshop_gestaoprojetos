from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from .models import Cliente
from .models import Colaborador

@login_manager.user_loader
def load_user(user_id):
    user = Cliente.query.get(int(user_id)) or Colaborador.query.get(int(user_id))
    return user

app.config.from_object(__name__)
from app import views

