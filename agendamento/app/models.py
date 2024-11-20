from app.app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name
    
class Agendamento(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    tipo_servico = db.Column(db.String(50), nullable=False)
    horario = db.Column(db.DateTime, nullable=False)
    
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'), nullable=False)
    colaborador = db.relationship('Colaborador', backref=db.backref('agendamentos', lazy=True))

    def __repr__(self):
        return f'<Agendamento {self.id}>'

class Colaborador(db.Model):
    __tablename__ = 'colaborador'

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

    def __repr__(self):
        return f'<Atendente {self.nome}>'