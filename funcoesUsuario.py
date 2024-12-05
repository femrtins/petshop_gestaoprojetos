from bd import *

if __name__ == "__main__":

    with app.app_context():
        # Criando o banco de dados
        db.create_all()
        app.run(debug=True)

        @app.route("/cadastrarCliente", methods=['POST'])
        def cadastroCliente():

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
        @login_required
        def cadastroColaborador():
            if current_user.cargo == "root":
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
            return "Você não tem permissão"

        @app.route("/cadastrarAnimal", methods=['POST'])
        @login_required
        def cadastrarAnimal():

            pet = Pet()

            pet.clienteId = current_user.id
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
                    login_user(cliente)
                    return "True"
                return "False"
            colaborador = db.session.query(Colaborador).filter(Colaborador.email == email).first()
            if colaborador != None:
                if colaborador.senha == senha:
                    login_user(colaborador)
                    return "True"
                return "False"
            
            return "Email não cadastrado"
        
        @app.route("/alterarDados", methods=['POST'])
        def alterarDados():

            nome = request.form.get("nome")
            endRua = request.form.get("rua")
            endNumero = request.form.get("numero")
            endComplemento = request.form.get("complemento")
            senha = request.form.get("senha")
            telefone = request.form.get("telefone")

            if nome:
                current_user.nome = nome
            if endRua:
                current_user.endRua = endRua
            if endNumero:
                current_user.endNumero = endNumero
            if endComplemento:
                current_user.endComplemento = endComplemento
            if senha:
                current_user.senha = senha
            if telefone:
                current_user.telefone = telefone

            try:
                db.session.commit()
                return "Alterado"
            except:
                return "Erro"
            
        @app.route('/deslogar')
        @login_required
        def deslogar():
            logout_user()
            return "True"