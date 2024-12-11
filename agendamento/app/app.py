from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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
def load_user(cliente_id):
    return Cliente.query.get(int(cliente_id))

@login_manager.user_loader
def load_user(colaborador_id):
    return Colaborador.query.get(int(colaborador_id))

app.config.from_object(__name__)
from app import views
