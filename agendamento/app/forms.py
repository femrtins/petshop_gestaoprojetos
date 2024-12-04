from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional, Regexp
from datetime import datetime

ano_atual = datetime.now().year

class ClienteForm(FlaskForm):
    def __init__(self, is_editing=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_editing = is_editing

        # Ajuste para a validação da senha, se estiver alterando os dados não exige que o valor da senha seja alterado
        if self.is_editing:
            self.senha.validators = [Optional(), Length(min=6, max=100)]
            self.confirmar_senha.validators = [Optional()]
        else:
            self.senha.validators = [DataRequired(), Length(min=6, max=100), EqualTo('confirmar_senha', message='As senhas devem coincidir.')]
            self.confirmar_senha.validators = [DataRequired()]
        
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(max=100)])
    celular = StringField('Celular', validators=[DataRequired(), Regexp(r"^\(?\d{2}\)?[-.\s]?\d{4,5}[-.\s]?\d{4}$")])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11, message="O CPF deve ter 11 caracteres.")])
    endRua = StringField('Endereço - Rua', validators=[Optional(), Length(max=80)])
    endNumero = IntegerField('Endereço - Número', validators=[Optional()])
    endComplemento = StringField('Endereço - Complemento', validators=[Optional(), Length(max=20)])
    temAnimal = BooleanField('Tem Animal? (Sim/Não)')
    
    senha = PasswordField('Senha')
    confirmar_senha = PasswordField('Confirmar Senha')

class ColaboradorForm(FlaskForm):
    def __init__(self, is_editing=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_editing = is_editing

        # Ajuste para a validação da senha, se estiver alterando os dados não exige que o valor da senha seja alterado
        if self.is_editing:
            self.senha.validators = [Optional(), Length(min=6, max=100)]
            self.confirmar_senha.validators = [Optional()]
        else:
            self.senha.validators = [DataRequired(), Length(min=6, max=100), EqualTo('confirmar_senha', message='As senhas devem coincidir.')]
            self.confirmar_senha.validators = [DataRequired()]

        
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(max=100)])
    celular = StringField('Celular', validators=[DataRequired(), Regexp(r"^\(?\d{2}\)?[-.\s]?\d{4,5}[-.\s]?\d{4}$")])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min=11, max=11, message="O CPF deve ter 11 caracteres.")])
    endRua = StringField('Endereço - Rua', validators=[Optional(), Length(max=80)])
    endNumero = IntegerField('Endereço - Número', validators=[Optional()])
    endComplemento = StringField('Endereço - Complemento', validators=[Optional(), Length(max=20)])
    
    senha = PasswordField('Senha')
    confirmar_senha = PasswordField('Confirmar Senha')
        
    cargo = SelectField('Cargo', choices=[('Veterinário', 'Veterinário'),('Assistente', 'Assistente'),], validators=[DataRequired()])    
    salario = FloatField('Salário', validators=[DataRequired(), NumberRange(min=0, message="O salário deve ser positivo.")])
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
    
class PetForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(max=100)])
    especie = StringField('Espécie', validators=[DataRequired(), Length(max=50)])
    raca = StringField('Raça', validators=[DataRequired(), Length(max=50)])
    anoNasc = IntegerField("Ano de Nascimento",validators=[NumberRange(min=1900, max=ano_atual,)])
    cliente_id = SelectField('Cliente', coerce=int)
