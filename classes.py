class Pessoa:
    def __init__(self, nome:str, cpf:int, email:str, dataNas:str, rua:str, numero:int, complemento:str, senha:str, telefone:str) -> None:
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.dataNas = dataNas
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.senha = senha
        self.telefone = telefone


class Cliente(Pessoa):
    def __init__(self, nome:str, cpf:int, email:str, dataNas:str, rua:str, numero:int, complemento:str, senha:str, telefone:str) -> None:
        super().__init__(nome, cpf, email, dataNas, rua, numero, complemento, senha, telefone)
        self.animais = []


class Colaborador(Pessoa):
    def __init__(self, nome: str, cpf: int, email: str, dataNas: str, rua: str, numero: int, complemento: str, 
                 senha: str, telefone: str, cargo:str, salario:float, status:bool, admin:bool) -> None:
        super().__init__(nome, cpf, email, dataNas, rua, numero, complemento, senha, telefone)
        self.cargo = cargo
        self.salario = salario
        self.status = status
        self.admin = admin


class Animal:
    def __init__(self, nome:str, especie:str, raca:str, anoNas:int) -> None:
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.anoNas = anoNas


class Servico:
    def __init__(self, id:int, tipo:str, cliente:Cliente, colaborador:Colaborador, descricao:str, valor:float) -> None:
        self.id = id
        self.tipo = tipo
        self.cliente = cliente
        self.colaborador = colaborador
        self.descricao = descricao
        self.valor = valor


class Produto:
    def __init__(self, id:int, nome:str, descricao:str, precoCusto:float, quantidade:int) -> None:
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.precoCusto = precoCusto
        self.quantidade = quantidade


class Medico(Colaborador):
    def __init__(self, nome: str, cpf: int, email: str, dataNas: str, rua: str, numero: int, complemento: str, senha: str, 
                 telefone: str, cargo: str, salario: float, status: bool, admin: bool, crmv:str) -> None:
        super().__init__(nome, cpf, email, dataNas, rua, numero, complemento, senha, telefone, cargo, salario, status, admin)
        self.crmv = crmv
