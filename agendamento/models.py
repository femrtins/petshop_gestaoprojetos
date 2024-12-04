from app.app import db
from flask_login import UserMixin    

class Agendamento(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    tipo_servico = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.DateTime, nullable=False)
    
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    colaborador = db.relationship('Colaborador', backref=db.backref('agendamentos', lazy=True))

class Cliente(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True , nullable=False)
    celular = db.Column(db.String(11))
    cpf = db.Column(db.String(11), unique=True , nullable=False)
    endRua = db.Column(db.String(80), nullable=True)
    endNumero = db.Column(db.Integer, nullable=True)
    endComplemento = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)    
    temAnimal = db.Column(db.Boolean, nullable=True)
      
class Pet(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    clienteId = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50))
    raca = db.Column(db.String(50))
    anoNasc = db.Column(db.Integer)

class Colaborador(UserMixin, db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True , nullable=False)
    celular = db.Column(db.String(11))
    cpf = db.Column(db.String(11), unique=True , nullable=False)
    endRua = db.Column(db.String(80), nullable=True)
    endNumero = db.Column(db.Integer, nullable=True)
    endComplemento = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)    
    telefone = db.Column(db.String(11), nullable=True)
    cargo = db.Column(db.String(50), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

class Estoque(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    qnt = db.Column(db.Integer, nullable=False) 
    tipo_produto = db.Column(db.String(50))
    preco_custo = db.Column(db.Float, nullable=False)
    validade = db.Column(db.Date)