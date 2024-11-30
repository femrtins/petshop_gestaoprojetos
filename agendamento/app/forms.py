from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional, Regexp
from datetime import datetime

class ColaboradorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11, message="O CPF deve ter 11 caracteres.")])
    endRua = StringField('Endereço - Rua', validators=[Optional(), Length(max=80)])
    endNumero = IntegerField('Endereço - Número', validators=[Optional()])
    endComplemento = StringField('Endereço - Complemento', validators=[Optional(), Length(max=20)])
    senha = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6, max=100),
        EqualTo('confirmar_senha', message='As senhas devem coincidir.')
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired()])
    cargo = StringField('Cargo', validators=[DataRequired(), Length(max=50)])
    salario = FloatField('Salário', validators=[DataRequired(), NumberRange(min=0, message="O salário deve ser positivo.")])
    status = BooleanField('Status (Ativo/Inativo)')
    
class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    celular = StringField('Celular', validators=[DataRequired(), Regexp(r"^\(?\d{2}\)?[-.\s]?\d{4,5}[-.\s]?\d{4}$")])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11, message="O CPF deve ter 11 caracteres.")])
    endRua = StringField('Endereço - Rua', validators=[Optional(), Length(max=80)])
    endNumero = IntegerField('Endereço - Número', validators=[Optional()])
    endComplemento = StringField('Endereço - Complemento', validators=[Optional(), Length(max=20)])
    senha = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6, max=100),
        EqualTo('confirmar_senha', message='As senhas devem coincidir.')
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired()])
    
    status = BooleanField('Status (Ativo/Inativo)')

class AgendamentoForm(FlaskForm):
    cliente = StringField('Nome do Cliente', validators=[DataRequired(), Length(min=2, max=100)])
    tipo_servico = SelectField('Tipo de Serviço', choices=[
        ('Consulta', 'Consulta'),
        ('Vacinação', 'Vacinação'),
        ('Exame Laboratorial', 'Exame Laboratorial'),
        ('Tosa', 'Tosa'),
        ('Banho', 'Banho')
    ], validators=[DataRequired()])

    data = DateField('Data do Agendamento', 
                     format='%Y-%m-%d', 
                     validators=[DataRequired()],
                     default=datetime.today)  
    
    horario = SelectField('Hora do Agendamento', 
                          choices=[
                              ('08:00', '08:00'),
                              ('09:00', '09:00'),
                              ('10:00', '10:00'),
                              ('11:00', '11:00'),
                              ('12:00', '12:00'),
                              ('13:00', '13:00'),
                              ('14:00', '14:00'),
                              ('15:00', '15:00'),
                              ('16:00', '16:00'),
                              ('17:00', '17:00')
                          ], validators=[DataRequired()])
    colaborador = SelectField('Atendente', coerce=int, validators=[DataRequired()])
    