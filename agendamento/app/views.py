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

@app.route('/del-agendamento', methods=['POST', 'GET'])
def del_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    try:
        db.session.delete(agendamento)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Ocorreu um erro ao excluir o agendamento: {str(e)}')
    
    return redirect(url_for('listar_agendamentos'))

@app.route('/edit-agendamento/<int:id>', methods=['POST', 'GET'])
def edit_agendamento(id):
    form = AgendamentoForm()    
    colaboradores = Colaborador.query.all()
    form.colaborador.choices = [(colaborador.id, colaborador.nome) for colaborador in colaboradores]
    agendamento = Agendamento.query.get_or_404(id)

    if request.method == 'POST':

        cliente = form.cliente.data
        tipo_servico = form.tipo_servico.data            
        data = form.data.data 
        horario_str = form.horario.data 
        colaborador = form.colaborador.data

        if data < datetime.today().date():
                flash("Não é possível agendar para datas passadas. Escolha uma data válida.", "danger")
                return redirect(url_for('agendar'))

        
        # Atualiza as informações do usuário
        if cliente:
            agendamento.cliente = cliente
        if tipo_servico:   
            agendamento.tipo_servico = tipo_servico      
        if data and horario:
            try:
                horario = datetime.combine(data, datetime.strptime(horario_str, '%H:%M').time())
            except ValueError:
                flash("Erro ao combinar data e hora. Tente novamente.", "danger")
                return redirect(url_for('agendar'))  
            
            if Agendamento.query.filter((Agendamento.colaborador_id == colaborador) & (Agendamento.horario >= horario - timedelta(hours=1)) & 
                                    (Agendamento.horario <= horario + timedelta(hours=1))).first():
                flash("Esse horário já está ocupado para o atendente selecionado. Escolha outro horário ou outro atendente.", "danger")
                return redirect(url_for('agendar'))            
            agendamento.horario = horario              
        if colaborador:
            agendamento.colaborador = colaborador
        
        # Salva as alterações no banco de dados
        try:
            db.session.commit()
            flash('Informações do perfil atualizadas com sucesso!')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao atualizar o perfil: {str(e)}')
    return redirect(url_for('listar_agendamentos'))


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