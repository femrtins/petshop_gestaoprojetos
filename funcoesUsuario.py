from config import *

if __name__ == "__main__":

    # Criando o banco de dados
    db.create_all()

    @app.route("/cadastrarCliente", methods=['POST'])
    def cadastroCliente():
        dados = request.get_json()
        resposta = jsonify({"resultado": "Cliente cadastrado", "detalhes": "ok"})
        cliente = Cliente(**dados)
        try:
            # Verifica se o cliente já foi cadastrado
            # db.session... Retorna 'None' caso não encontre nada 
            if  ((db.session.query(Cliente).filter(Cliente.email == dados["email"]).first()) or \
                (db.session.query(Cliente).filter(Cliente.cpf == dados["cpf"]).first())) != None :
                return jsonify({"resultado": "Erro", "detalhes": "Cliente com CPF ou email já cadastrado"})

            db.session.add(cliente)
            db.session.commit()
            print("Colaborador incluido")

        except Exception as e:
            
            resposta = jsonify({"resultado": "erro", "detalhes": str(e)})
            print("Colaborador rejeitado")

        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
    

    @app.route("/cadastrarColaborador", methods=['POST'])
    def cadastroCliente():
        dados = request.get_json()
        resposta = jsonify({"resultado": "Colaborador cadastrado", "detalhes": "ok"})
        colaborador = Colaborador(**dados)
        try:

            '''
            
            Precisa verificar se o colaborador que está adicionando outro é o adminitrador root
            
            '''

            # Verifica se o colaborador já foi cadastrado
            # db.session... Retorna 'None' caso não encontre nada 
            if  ((db.session.query(Colaborador).filter(Colaborador.email == dados["email"]).first()) or \
                (db.session.query(Colaborador).filter(Colaborador.cpf == dados["cpf"]).first())) != None :
                return jsonify({"resultado": "Erro", "detalhes": "Colaborador com CPF ou email já cadastrado"})

            db.session.add(colaborador)
            db.session.commit()
            print("Colaborador incluido")

        except Exception as e:
            
            resposta = jsonify({"resultado": "erro", "detalhes": str(e)})
            print("Colaborador rejeitado")

        resposta.headers.add("Access-Control-Allow-Origin", "*")
        return resposta
