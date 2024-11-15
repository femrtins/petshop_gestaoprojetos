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

create_table_stock()

