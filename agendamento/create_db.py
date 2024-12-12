from app import db, app
from app.models import Colaborador, Cliente
from werkzeug.security import generate_password_hash

with app.app_context():
    # Criação das tabelas
    db.create_all()
    print("Tabelas criadas com sucesso!")

    admin_existente = Colaborador.query.filter_by(email="admin@gmail.com").first()
    if not admin_existente:
        admin = Colaborador(
            nome="admin",
            email="admin@gmail.com",
            celular="11999999999",
            cpf="12345678901",
            endRua=" ",
            endNumero=1,
            endComplemento=" ",
            senha= "123",
            cargo="Gerente",
            salario=00.00,
            status=True
        )
        db.session.add(admin)
        db.session.commit()
    colaborador_existente = Colaborador.query.filter_by(email="colaborador@gmail.com").first()
    if not colaborador_existente:
        colaborador = Colaborador(
            nome="Colaborador",
            email="colaborador@gmail.com",
            celular="11999999999",
            cpf="12345671901",
            endRua=" ",
            endNumero=1,
            endComplemento=" ",
            senha= "123",
            cargo="Médico",
            salario=00.00,
            status=True
        )
        db.session.add(colaborador)
        db.session.commit()
    cliente_existente = Cliente.query.filter_by(email="cliente@gmail.com").first()
    if not cliente_existente:
        cliente = Cliente(
            nome="Cliente",
            email="cliente@gmail.com",
            celular="11999999999",
            cpf="10987654321",
            senha="123",
            temAnimal=True
        )
        db.session.add(cliente)
        db.session.commit()
        
        
        
        
        print("Admin e cliente criados com sucesso!")
    else:
        print("Admin já existe no banco de dados.")
