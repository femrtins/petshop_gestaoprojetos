from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Cria o arquivo do banco de dados
diretorio = os.path.dirname(os.path.abspath(__file__))
arquivobanco = os.path.join(diretorio, "bancodados.db")

# Configura o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + arquivobanco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)