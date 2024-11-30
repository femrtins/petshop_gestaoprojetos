from app.app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import AgendamentoForm, ColaboradorForm
from app.models import Agendamento, Colaborador
from datetime import timedelta, datetime

###
# Rotas da aplicação
###



# Rota para listar os agendamentos (home)

@app.route('/', methods=['GET', 'POST'])
def listar_agendamentos():
    colaborador_id = request.args.get('colaborador_id', type=int)
    colaboradores = Colaborador.query.all()

    if colaborador_id:
        agendamentos = Agendamento.query.filter_by(colaborador_id=colaborador_id).all()
    else:
        agendamentos = Agendamento.query.all()

    return render_template('lista_agendamentos.html', agendamentos=agendamentos, colaboradores=colaboradores, colaborador_id=colaborador_id)

# Rota para agendar um serviço

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    form = AgendamentoForm()
    
    colaboradores = Colaborador.query.all()
    form.colaborador.choices = [(colaborador.id, colaborador.nome) for colaborador in colaboradores]
    
    if request.method == 'POST':
        if form.validate_on_submit():
            
            cliente = form.cliente.data
            tipo_servico = form.tipo_servico.data            
            data = form.data.data 
            horario_str = form.horario.data 
            colaborador = form.colaborador.data

            if data < datetime.today().date():
                flash("Não é possível agendar para datas passadas. Escolha uma data válida.", "danger")
                return redirect(url_for('agendar'))

            try:
                horario = datetime.combine(data, datetime.strptime(horario_str, '%H:%M').time())
            except ValueError:
                flash("Erro ao combinar data e hora. Tente novamente.", "danger")
                return redirect(url_for('agendar'))

            if Agendamento.query.filter((Agendamento.colaborador_id == colaborador) & (Agendamento.horario >= horario - timedelta(hours=1)) & 
                                        (Agendamento.horario <= horario + timedelta(hours=1))).first():
                flash("Esse horário já está ocupado para o atendente selecionado. Escolha outro horário ou outro atendente.", "danger")
                return redirect(url_for('agendar'))
            
            novo_agendamento = Agendamento(cliente=cliente,tipo_servico=tipo_servico, horario=horario, colaborador_id = colaborador)
            db.session.add(novo_agendamento)
            db.session.commit()
            flash("Agendamento realizado com sucesso!", "success")
            return redirect(url_for('listar_agendamentos'))
        
    flash_errors(form)
    return render_template('agendar.html', form=form)

#  para adicionar um colaborador

@app.route('/add-colaborador', methods=['POST', 'GET'])
def add_colaborador():
    form = ColaboradorForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            
            nome = form.nome.data 
            email = form.email.data 
            cpf = form.cpf.data
            endRua = form.endRua.data
            endNumero = form.endNumero.data
            endComplemento = form.endComplemento.data
            senha = form.senha.data
            confSenha = form.confirmar_senha.data
            cargo = form.cargo.data
            salario = form.salario.data
            status = form.status.data
            
            if senha != confSenha:
                flash("As senhas não coincidem!")
                return redirect(url_for(add_colaborador))
            
            colaborador = Colaborador(nome=nome, email=email, cpf=cpf, endRua=endRua, endNumero=endNumero, endComplemento=endComplemento,
                                      senha=senha, cargo=cargo, salario=salario, status=status)
            db.session.add(colaborador)
            db.session.commit()

            flash('Colaborador adicionado com sucesso')
            return redirect(url_for('listar_agendamentos'))

    flash_errors(form)
    return render_template('add_colaborador.html', form=form)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Erro no campo %s - %s" % (
                getattr(form, field).label.text,
                error
            ))
            
####################################################################

@app.route("/cadastrarCliente", methods=['POST'])
def cadastroCliente():
    form = ClienteForm()
    cliente = Cliente()

    cliente.nome = request.form.get("nome")
    cliente.email = request.form.get("email")
    cliente.cpf = request.form.get("cpf")
    cliente.endRua = request.form.get("rua")
    cliente.endNumero = request.form.get("numero")
    cliente.endComplemento = request.form.get("complemento")
    cliente.senha = request.form.get("senha")
    cliente.telefone = request.form.get("telefone")
    
    try:
        # Verifica se o cliente já foi cadastrado
        # db.session... Retorna 'None' caso não encontre nada 
        if  ((db.session.query(Cliente).filter(Cliente.email == cliente.email).first() != None) or \
            (db.session.query(Cliente).filter(Cliente.cpf == cliente.cpf).first())!= None):
            return "Erro"

        db.session.add(cliente)
        db.session.commit()
        print("Colaborador incluido")

    except Exception as e:
        print(str(e))
        return "Erro"

    return "Sucesso"
    

@app.route("/cadastrarColaborador", methods=['POST'])
def cadastroCliente():
        
    colaborador = Colaborador()

    colaborador.nome = request.form.get("nome")
    colaborador.email = request.form.get("email")
    colaborador.cpf = request.form.get("cpf")
    colaborador.endRua = request.form.get("rua")
    colaborador.endNumero = request.form.get("numero")
    colaborador.endComplemento = request.form.get("complemento")
    colaborador.senha = request.form.get("senha")
    colaborador.telefone = request.form.get("telefone")
    colaborador.cargo = request.form.get("cargo")
    colaborador.salario = request.form.get("salario")
    colaborador.status = request.form.get("status")
    
    try:

        '''
        
        Precisa verificar se o colaborador que está adicionando outro é o adminitrador root
        
        '''

        # Verifica se o colaborador já foi cadastrado
        # db.session... Retorna 'None' caso não encontre nada 
        if  ((db.session.query(Colaborador).filter(Colaborador.email == colaborador.email).first()) or \
            (db.session.query(Colaborador).filter(Colaborador.cpf == colaborador.cpf).first())) != None :
            return "Erro"

        db.session.add(colaborador)
        db.session.commit()

        print("Colaborador incluido")

    except Exception as e:
        print(str(e))
        return "Erro"

    return "Sucesso"

@app.route("/cadastrarAnimal", methods=['POST'])
def cadastrarAnimal():

    pet = Pet()

    pet.clienteId = request.form.get("clienteId")
    pet.nome = request.form.get("nome")
    pet.especie = request.form.get("especia")
    pet.raca = request.form.get("raca")
    pet.anoNasc = request.form.get("anoNasc")

    try:
        
        db.session.add(pet)
        db.session.commit()
        print("Animal incluido")

    except Exception as e:
        print(str(e))
        return "Erro"

    return "Sucesso"

@app.route("/login", methods=['POST'])
def login():

    email = request.form.get("email")
    senha = request.form.get("senha")

    cliente = db.session.query(Cliente).filter(Cliente.email == email).first()
    if cliente != None:
        if cliente.senha == senha:
            return "True"
        return "False"
    colaborador = db.session.query(Colaborador).filter(Colaborador.email == email).first()
    if colaborador != None:
        if colaborador.senha == senha:
            return "True"
        return "False"
    
    return "Email não cadastrado"

@app.route("/alterarDados", methods=['POST'])
def alterarDados():
    pass