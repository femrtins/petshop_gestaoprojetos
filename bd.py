from flask_login import UserMixin
from config import *

class Cliente(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True , nullable=False)
    cpf = db.Column(db.String(11), unique=True , nullable=False)
    endRua = db.Column(db.String(80), nullable=True)
    endNumero = db.Column(db.Integer, nullable=True)
    endComplemento = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)    
    telefone = db.Column(db.String(11), nullable=True)
    
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
    cpf = db.Column(db.String(11), unique=True , nullable=False)
    endRua = db.Column(db.String(80), nullable=True)
    endNumero = db.Column(db.Integer, nullable=True)
    endComplemento = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)    
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

class ItemUtilizado(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estoqueID = db.Column(db.Integer, db.ForeignKey('estoque.id'), nullable=False)
    agendamentoID = db.Column(db.Integer, db.ForeignKey('agendamento.id'), nullable=False)
    qnt = db.Column(db.Integer, nullable=False) 

class Agendamento(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colaboradorID = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    petID = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    tipo = db.Column(db.String(1), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

class Servico(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agendamentoID = db.Column(db.Integer, db.ForeignKey('agendamento.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

class Consulta(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agendamentoID = db.Column(db.Integer, db.ForeignKey('agendamento.id'), nullable=False)
    laudo = db.Column(db.String(1000), nullable=False)

class Exame(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consultaID = db.Column(db.Integer, db.ForeignKey('consulta.id'), nullable=False)
    gendamentoID = db.Column(db.Integer, db.ForeignKey('agendamento.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)
    resultado = db.Column(db.String(1000), nullable=False)