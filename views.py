from app import app, db
from flask import render_template, request, redirect, url_for, flash, abort, jsonify, session
from forms import AgendamentoForm, ColaboradorForm, ClienteForm, PetForm, AgendamentoEditForm
from models import Agendamento, Colaborador, Cliente, Pet, Estoque
from datetime import datetime
from flask_login import login_required, current_user, logout_user, login_user
from functools import wraps

###
# Rotas da aplicação
###

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verifica se o usuário é um Colaborador ou se tem o e-mail de admin
        if current_user.email != "admin@example.com":
            abort(403)  
        return func(*args, **kwargs)
    return wrapper


def colaborador_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verifica se o usuário atual tem o papel de 'colaborador'
        if getattr(current_user, 'role', None) != 'colaborador':
            abort(403)  # Acesso proibido
        return func(*args, **kwargs)
    return wrapper

# Rota para listar os agendamentos

@app.route('/', methods=['GET', 'POST'])
@login_required
def listar_agendamentos():
    # Obtém os parâmetros de filtro
    colaborador_id = request.args.get('colaborador_id', type=int)
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')
    
    # Filtra agendamentos com base no papel do usuário
    query = Agendamento.query
    
    if current_user.role == 'cliente':
        query = query.filter(Agendamento.cliente_id == current_user.id)
    elif current_user.role == 'colaborador':
        if colaborador_id:
            query = query.filter(Agendamento.colaborador_id == colaborador_id)
    
    # Aplica os filtros de data
    if data_inicial:
        query = query.filter(Agendamento.horario >= datetime.strptime(data_inicial, '%Y-%m-%d'))
    if data_final:
        query = query.filter(Agendamento.horario <= datetime.strptime(data_final, '%Y-%m-%d'))
    
    # Ordena por horário crescente e executa a consulta
    agendamentos = query.order_by(Agendamento.horario).all()

    # Para colaboradores, carrega a lista de colaboradores
    colaboradores = Colaborador.query.all() if current_user.role == 'colaborador' else []

    return render_template(
        'lista_agendamentos.html', 
        agendamentos=agendamentos, 
        colaboradores=colaboradores, 
        colaborador_id=colaborador_id,
        data_inicial=data_inicial,
        data_final=data_final
    )


# Rota para agendar um serviço

@app.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    form = AgendamentoForm()

    colaboradores = Colaborador.query.all()
    form.colaborador.choices = [(colaborador.id, colaborador.nome) for colaborador in colaboradores]
    
    if request.method == 'POST':
        if form.validate_on_submit():
            
            tipo_servico = form.tipo_servico.data            
            data = form.data.data 
            horario_str = form.horario.data 
            colaborador = form.colaborador.data
            
            if current_user.role == 'cliente':
                cliente_id = current_user.id
            else:
                cliente_id = form.cliente.data  

            if data < datetime.today().date():
                flash("Não é possível agendar para datas passadas. Escolha uma data válida.", "danger")
                return redirect(url_for('agendar'))
            try:
                horario = datetime.combine(data, datetime.strptime(horario_str, '%H:%M').time())
            except ValueError:
                flash("Erro ao combinar data e hora. Tente novamente.", "danger")
                return redirect(url_for('agendar'))

            if Agendamento.query.filter((Agendamento.colaborador_id == colaborador) & (Agendamento.horario == horario)).first():
                flash("Esse horário já está ocupado para o atendente selecionado. Escolha outro horário ou outro atendente.", "danger")
                return redirect(url_for('agendar'))

            
            novo_agendamento = Agendamento(tipo_servico=tipo_servico, horario=horario,cliente_id=cliente_id, colaborador_id = colaborador)
            db.session.add(novo_agendamento)
            db.session.commit()
            return redirect(url_for('listar_agendamentos'))
        
    flash_errors(form)
    return render_template('agendar.html', form=form)

@app.route('/del-agendamento/<int:id>', methods=['POST'])
def del_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    try:
        db.session.delete(agendamento)
        db.session.commit()
        flash("Agendamento excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ocorreu um erro ao excluir o agendamento: {str(e)}", "danger")
    return redirect(url_for('listar_agendamentos'))

@app.route('/edit-agendamento/<int:id>', methods=['GET', 'POST'])
def edit_agendamento(id):
    form = AgendamentoEditForm()
    colaboradores = Colaborador.query.all()
    form.colaborador.choices = [(colaborador.id, colaborador.nome) for colaborador in colaboradores]
    agendamento = Agendamento.query.get_or_404(id)
    if current_user.role == 'colaborador':
        form.cliente.render_kw = {'readonly': True}
    

    if request.method == 'POST':
        tipo_servico = form.tipo_servico.data
        data = form.data.data
        horario_str = form.horario.data
        colaborador = form.colaborador.data


        if current_user.role == 'cliente':
            cliente_id = current_user.id
        else:
            cliente_id = form.cliente.data  
            print(cliente_id) 

        # Validação de data
        if data < datetime.today().date():
            flash("Não é possível agendar para datas passadas. Escolha uma data válida.", "danger")
            return redirect(url_for('edit_agendamento', id=id))

        try:
            horario = datetime.combine(data, datetime.strptime(horario_str, '%H:%M').time())
        except ValueError:
            flash("Erro ao combinar data e hora. Tente novamente.", "danger")
            return redirect(url_for('edit_agendamento', id=id))

        # Verifica conflitos de horários
        if Agendamento.query.filter(
            (Agendamento.colaborador_id == colaborador) & (Agendamento.horario == horario) & (Agendamento.id != id) ).first():
            flash("Esse horário já está ocupado para o atendente selecionado. Escolha outro horário ou outro atendente.", "danger")
            return redirect(url_for('edit_agendamento', id=id))

        # Atualização dos campos
        agendamento.cliente_id = cliente_id
        agendamento.tipo_servico = tipo_servico
        agendamento.horario = horario
        agendamento.colaborador_id = colaborador

        # Salva no banco de dados
        try:
            db.session.commit()
            flash("Agendamento atualizado com sucesso!", "success")
            return redirect(url_for('listar_agendamentos'))
        except Exception as e:
            db.session.rollback()
            flash(f"Ocorreu um erro ao salvar as alterações: {str(e)}", "danger")

    form.cliente.data = agendamento.cliente_id
    form.tipo_servico.data = agendamento.tipo_servico
    form.data.data = agendamento.horario.date()
    form.horario.data = agendamento.horario.strftime('%H:%M')
    form.colaborador.data = agendamento.colaborador_id

    return render_template('edit_agendamento.html', form=form, agendamento=agendamento)

#  para adicionar um colaborador

@app.route('/cadastrarColaborador', methods=['POST', 'GET'])
@login_required
@admin_required
def cadastroColaborador():
    print(current_user)

    form = ColaboradorForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            
            nome = form.nome.data 
            email = form.email.data 
            celular = form.celular.data
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
                return redirect(url_for('cadastroColaborador'))
            
            colaborador = Colaborador(nome=nome, email=email, celular=celular, cpf=cpf, endRua=endRua, endNumero=endNumero, endComplemento=endComplemento,
                                      senha=senha, cargo=cargo, salario=salario, status=status)
            
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
                flash('Colaborador adicionado com sucesso')

            except Exception as e:
                print(str(e))
                return "Erro"

            return redirect(url_for('index'))

    flash_errors(form)
    return render_template('cadastroColaborador.html', form=form)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Erro no campo %s - %s" % (
                getattr(form, field).label.text,
                error
            ))

####################################################################

@app.route("/cadastrarCliente",  methods=['POST', 'GET'])
def cadastroCliente():
    if request.method == 'POST':                

            
        nome = request.form.get("nome") 
        email = request.form.get("email") 
        cpf = request.form.get("cpf")
        celular = request.form.get("celular")
        endRua = request.form.get("rua")
        endNumero = request.form.get("numero")
        endComplemento = request.form.get("bairro")
        senha = request.form.get("senha")
        confSenha = request.form.get("confirmar-senha")
        temAnimal = True
        
        if senha != confSenha:
            flash("As senhas não coincidem!")
            return redirect(url_for('cadastro'))
        
        cliente = Cliente(nome=nome, email=email, cpf=cpf, celular=celular, endRua=endRua, endNumero=endNumero, endComplemento=endComplemento, senha=senha, temAnimal=temAnimal)
        
        try:
            # Verifica se o colaborador já foi cadastrado
            # db.session... Retorna 'None' caso não encontre nada 
            if db.session.query(Cliente).filter(Cliente.email == cliente.email).first():
                flash("O e-mail já está cadastrado!", "danger")
                return redirect(url_for('cadastro'))
            if db.session.query(Cliente).filter(Cliente.cpf == cliente.cpf).first():
                flash("O CPF já está cadastrado!", "danger")
                return redirect(url_for('cadastro'))

            db.session.add(cliente)
            db.session.commit()
            flash('Cliente adicionado com sucesso')
        except Exception as e:
            print(str(e))
            return "Erro"
        
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')



@app.route("/cadastrarAnimal", methods=['POST', 'GET'])
@login_required
def cadastroPet():
    form = PetForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            pet = Pet()
            pet.clienteId = current_user.id
            pet.nome = form.nome.data 
            pet.especie = form.especie.data 
            pet.raca = form.raca.data 
            pet.anoNasc = form.anoNasc.data 

        try:
            db.session.add(pet)
            db.session.commit()
            print("Animal incluido")

        except Exception as e:
            print(str(e))
            return "Erro"

        return redirect(url_for('index'))

    flash_errors(form)
    return render_template('cadastroPet.html', form=form)

@app.route("/alterarDadosColaborador/<int:id>", methods=['POST', 'GET'])
@login_required
@colaborador_required
def alterarDadosColaborador(id):
    # Verifica se a rota está sendo acessada
    form = ColaboradorForm(is_editing=True)
    colaborador = Colaborador.query.get_or_404(id)

    if request.method == 'POST':
        # Verifica se o formulário é válido
        if form.validate_on_submit():
        
            nome = form.nome.data 
            celular = form.celular.data
            endRua = form.endRua.data
            endNumero = form.endNumero.data
            endComplemento = form.endComplemento.data
            cargo = form.cargo.data
            salario = form.salario.data
            status = form.status.data

            # Atualiza os dados do colaborador
            colaborador.nome = nome
            colaborador.celular = celular
            colaborador.endRua = endRua
            colaborador.endNumero = endNumero
            colaborador.endComplemento = endComplemento
            colaborador.cargo = cargo
            colaborador.salario = salario
            colaborador.status = status

            # Tenta salvar as alterações no banco de dados
            try:
                db.session.commit()
                flash("Colaborador atualizado com sucesso!", "success")
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f"Ocorreu um erro ao salvar as alterações: {str(e)}", "danger")
                print("Erro ao salvar:", str(e))

    # Preenche o formulário com os dados atuais do colaborador
    form.nome.data = colaborador.nome
    form.email.data = colaborador.email  # Não altere o email no formulário
    form.celular.data = colaborador.celular
    form.cpf.data = colaborador.cpf  # Não altere o CPF no formulário
    form.endRua.data = colaborador.endRua
    form.endNumero.data = colaborador.endNumero
    form.endComplemento.data = colaborador.endComplemento
    form.cargo.data = colaborador.cargo
    form.salario.data = colaborador.salario
    form.status.data = colaborador.status
    form.senha.data = ''
    form.confirmar_senha.data = ''

    return render_template('alterarDadosColaborador.html', form=form)

@app.route("/alterarDadosCliente/<int:id>", methods=['POST', 'GET'])
@login_required
def alterarDadosCliente(id):
    # Verifica se a rota está sendo acessada
    form = ClienteForm(is_editing=True)
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        # Verifica se o formulário é válido
        if form.validate_on_submit():
        
            nome = form.nome.data 
            celular = form.celular.data
            endRua = form.endRua.data
            endNumero = form.endNumero.data
            endComplemento = form.endComplemento.data
            temAnimal = form.temAnimal.data

            # Atualiza os dados do colaborador
            cliente.nome = nome
            cliente.celular = celular
            cliente.endRua = endRua
            cliente.endNumero = endNumero
            cliente.endComplemento = endComplemento
            cliente.temAnimal = temAnimal

            # Tenta salvar as alterações no banco de dados
            try:
                db.session.commit()
                flash("Cliente atualizado com sucesso!", "success")
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f"Ocorreu um erro ao salvar as alterações: {str(e)}", "danger")
                print("Erro ao salvar:", str(e))

    # Preenche o formulário com os dados atuais do colaborador
    form.nome.data = cliente.nome
    form.email.data = cliente.email  # Não altere o email no formulário
    form.celular.data = cliente.celular
    form.cpf.data = cliente.cpf  # Não altere o CPF no formulário
    form.endRua.data = cliente.endRua
    form.endNumero.data = cliente.endNumero
    form.endComplemento.data = cliente.endComplemento
    form.temAnimal.data = cliente.temAnimal
    form.senha.data = ''
    form.confirmar_senha.data = ''

    return render_template('alterarDadosCliente.html', form=form)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        senha = request.form.get("senha")
        cliente = False
        colaborador = False
        try:
            cliente = db.session.query(Cliente).filter(Cliente.email == email).first()
        except:
            pass
        if cliente:
            if cliente.senha == senha:
                login_user(cliente)
                return redirect(url_for('index'))

        else:
            try:
                colaborador = db.session.query(Colaborador).filter(Colaborador.email == email).first()
            except:
                pass
            if colaborador:
                if colaborador.senha == senha:
                    login_user(colaborador)
                    return redirect(url_for('index'))
            else:
                flash("Email não encontrado.", "danger")

    return render_template('index.html')

@app.route('/deslogar')
@login_required
def deslogar():
    logout_user()
    return render_template('index.html')

##########################################################


@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/stock_add")
@login_required
@colaborador_required
def stock_add_page():    
    return render_template('stock_add.html')

@app.route("/submit-stock", methods=['POST'])
@login_required
@colaborador_required
def submit_stock():
    
    #   Recuperando os dados do formulario
    name = request.form.get('item-name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    category = request.form.get('category')
    description = request.form.get('description')

    #   O BD não pode receber nada com " ou ' porque quebraria o query
    name = name.replace("'", "")
    name = name.replace('"', "")

    description = description.replace("'", "")
    description = description.replace('"', "")

    item = Estoque(nome=name, qnt=quantity, preco_custo=price, categoria=category, descricao=description)
    
    try:
        db.session.add(item)
        db.session.commit()

    except Exception as e:
        print(str(e))
        return "Erro"

    return redirect("/stock")

@app.route("/stock")
@login_required
@colaborador_required
def stock_view():
    estoque = Estoque.query.all()

    return render_template("stock.html", data=estoque)

@app.route("/edit_stock/<int:item_id>", methods=['GET', 'POST'])
@login_required
@colaborador_required
def editar_item(item_id):
    item = Estoque.query.get_or_404(item_id)

    if request.method == 'POST':
        # Recuperar os dados do formulário
        name = request.form.get('item-name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        category = request.form.get('category')
        description = request.form.get('description')

        # Sanitizar os dados para evitar problemas com aspas
        if name:
            name = name.replace("'", "").replace('"', "")
        if description:
            description = description.replace("'", "").replace('"', "")

        # Atualizar os campos do item
        item.nome = name or item.nome
        item.qnt = quantity or item.qnt
        item.preco_custo = price or item.preco_custo
        item.categoria = category or item.categoria
        item.descricao = description or item.descricao

        try:
            # Salvar as alterações no banco de dados
            db.session.commit()
            return redirect("/stock")
        except Exception as e:
            print(str(e))
            return "Erro ao editar o item do estoque."

    # Renderizar o formulário de edição com os dados do item
    return render_template('edit_stock.html', item_data=item)



@app.route('/delete-item/<int:item_id>', methods=['GET'])
@login_required
@colaborador_required
def delete_stock(item_id):
    estoque = Estoque.query.get_or_404(item_id)
    try:
        db.session.delete(estoque)
        db.session.commit()
        flash("Item excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ocorreu um erro ao excluir o item: {str(e)}", "danger")

    return redirect('/stock')


# ##################################################################

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

