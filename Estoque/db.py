import sqlite3


con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()


def create_table_stock():
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS STOCK (
                        PK_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                        NOME TEXT, 
                        QUANTIDADE_DISPONIVEL INTEGER, 
                        PRECO INTEGER, 
                        CATEGORIA TEXT,
                        DESCRICAO TEXT 
                                                            );""")
        
        con.commit()
    except:
        print("erro ao criar a tabela de estoque")


def add_to_stock(name, quantity, price, category, description):
    try:
        cur.execute(f"INSERT INTO STOCK (NOME, QUANTIDADE_DISPONIVEL, PRECO, CATEGORIA, DESCRICAO) VALUES \
                ('{name}', {quantity}, {price} ,'{category}', '{description}')")

        con.commit() 
    except:
        print("erro ao adicionar na tabela STOCK")


def fetch_data():
    cur.execute("SELECT * FROM STOCK")
    raw_data = cur.fetchall()
    listed_data = []

    for i in raw_data:
        listed_data.append(i)

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
    cur.execute(f"SELECT * FROM STOCK WHERE PK_ID= {id};")


    raw_data = cur.fetchall()

    return (raw_data[0])

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
    cur.execute(f"UPDATE STOCK SET NOME = '{item['Nome']}', \
                QUANTIDADE_DISPONIVEL = {item['qnt']}, \
                PRECO = {item['preco']}, \
                CATEGORIA = '{item['categoria']}',\
                DESCRICAO = '{item['descricao']}'\
                WHERE PK_ID = {item['id']}")
    
    con.commit()


def remove_item(item):
    cur.execute(f"DELETE FROM STOCK WHERE PK_ID = {item};")

    con.commit()

create_table_stock()

