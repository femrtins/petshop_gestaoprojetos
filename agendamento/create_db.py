from app.app import db, app
from app.models import Colaborador 

# Dados do colaborador a ser criado
novo_colaborador = {
    "nome": "admin",
    "email": "admin@example.com",
    "celular": "11999999999",
    "cpf": "12345678901",
    "endRua": " ",
    "endNumero": 1,
    "endComplemento": " ",
    "senha": "123", 
    "cargo": "Gerente",
    "salario": 00.00,
    "status": True
}

with app.app_context():
    # Criação das tabelas
    db.create_all()
    print("Tabela 'colaborador' criada com sucesso!")

    # Verificar se o colaborador já existe (baseado no email ou CPF)
    colaborador_existente = Colaborador.query.filter_by(email=novo_colaborador["email"]).first()
    if not colaborador_existente:
        # Criar um novo colaborador
        colaborador = Colaborador(
            nome=novo_colaborador["nome"],
            email=novo_colaborador["email"],
            celular=novo_colaborador["celular"],
            cpf=novo_colaborador["cpf"],
            endRua=novo_colaborador["endRua"],
            endNumero=novo_colaborador["endNumero"],
            endComplemento=novo_colaborador["endComplemento"],
            senha=novo_colaborador["senha"],  # Em produção, use um hash seguro
            cargo=novo_colaborador["cargo"],
            salario=novo_colaborador["salario"],
            status=novo_colaborador["status"]
        )
        db.session.add(colaborador)
        db.session.commit()
        print("Colaborador criado com sucesso!")
    else:
        print("Colaborador já existe no banco de dados.")
