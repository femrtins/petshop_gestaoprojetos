from app.app import db
from flask_login import UserMixin    
from sqlalchemy.ext.declarative import declared_attr




class Agendamento(db.Model):
    __tablename__ = 'agendamento'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_servico = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.DateTime, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    colaborador = db.relationship('Colaborador', backref=db.backref('agendamentos', lazy=True))
    
    def get_nome_cliente(self):
        cliente = Cliente.query.get(self.cliente_id)
        return cliente.nome if cliente else None


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)  # ID compartilhado
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    celular = db.Column(db.String(11))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    endRua = db.Column(db.String(80), nullable=True)
    endNumero = db.Column(db.Integer, nullable=True)
    endComplemento = db.Column(db.String(20), nullable=True)
    senha = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',  # Identidade padrão para o modelo base
        'polymorphic_on': role  # Campo usado para diferenciar os tipos
    }

class Cliente(Usuario):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    temAnimal = db.Column(db.Boolean, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'cliente',  # Identidade para Cliente
    }

class Colaborador(Usuario):
    __tablename__ = 'colaborador'
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    cargo = db.Column(db.String(50), nullable=False)
    salario = db.Column(db.Float, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'colaborador',  # Identidade para Colaborador
    }
      
class Pet(UserMixin, db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key = True)
    clienteId = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50))
    raca = db.Column(db.String(50))
    anoNasc = db.Column(db.Integer)

class Estoque(UserMixin, db.Model):
    __tablename__ = 'estoque'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    qnt = db.Column(db.Integer, nullable=False) 
    categoria = db.Column(db.String(50))
    preco_custo = db.Column(db.Float, nullable=False)