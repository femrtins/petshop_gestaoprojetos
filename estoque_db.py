from config import db
from flask_sqlalchemy import SQLAlchemy
import bd


def add_to_stock(name, quantity, price, category, description):
    try:
        temp = bd.Estoque()
        temp.nome = name
        temp.qnt = quantity
        temp.preco_custo = price
        temp.tipo_produto = category
        temp.descricao = description

        db.session.add(temp)
        db.session.commit()
    
    except:
        print("erro ao adicionar na tabela STOCK")


def fetch_data():
    raw_data = bd.Estoque.query.all()
    listed_data = []

    for i in raw_data:
        temp = [i.id, i.nome, i.qnt, i.preco_custo, i.tipo_produto, i.descricao]
        listed_data.append(temp)

    return listed_data


def process_data(data):
    processed_data = []

    for i in data:
        dic_data = {"id":        i[0],
                    "Nome":      i[1],
                    "qnt":       i[2],
                    "preco":     i[3],
                    "categoria": i[4],
                    "descricao": i[5]
                    }
        processed_data.append(dic_data)

    return processed_data

def fetch_data_dic():
    return process_data(fetch_data())

def fetch_data_by_id(id: int):
    raw_data = bd.Estoque.query.filter_by(id=id).first()

    listed_data = [raw_data.id, raw_data.nome, raw_data.qnt, raw_data.preco_custo, raw_data.tipo_produto, raw_data.descricao]

    return (listed_data)

def item_to_dic(item):
    dic_data = {    "id":        item[0],
                    "Nome":      item[1],
                    "qnt":       item[2],
                    "preco":     item[3],
                    "categoria": item[4],
                    "descricao": item[5]
                    }
    
    return dic_data


def edit_by_id(item):
    obj = bd.Estoque.query.filter_by(id=item['id']).first()

    obj.nome = item['Nome']
    obj.qnt = item['qnt']
    obj.preco_custo = item['preco']
    obj.tipo_produto = item['categoria']
    obj.descricao = item['descricao']

    db.session.commit()


def remove_item(item):
    
    obj = bd.Estoque.query.filter_by(id=item['id']).first()

    db.session.delete(obj)
    db.session.commit()

