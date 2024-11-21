from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/stock_add")
def stock_add_page():
    if not checkUser():
        return redirect('/')
    
    return render_template('stock_add.html')

@app.route("/submit-stock", methods=['POST'])
def submit_stock():

    if not checkUser():
        return redirect('/')
    
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

    db.add_to_stock(name, quantity, price, category, description)

    return redirect("/stock")

@app.route("/stock")
def stock_view():

    if not checkUser():
        return redirect('/')

    data = db.fetch_data_dic()
    return render_template("stock.html", data=data)
    

@app.route("/edit_stock/<int:item_id>", methods=['GET'])
def editar_item(item_id):
    
    if not checkUser():
        return redirect('/')

    data = db.fetch_data_by_id(item_id)
    data = db.item_to_dic(data)

    return render_template("edit_stock.html", item_data=data)


@app.route('/update-stock', methods=['POST'])
def update_stock():
    
    if not checkUser():
        return redirect('/')

    data = {
        'id': request.form['item-id'],
        'Nome': request.form['item-name'],
        'qnt': int(request.form['quantity']),
        'preco': float(request.form['price']),
        'categoria': request.form['category'],
        'descricao': request.form['description']
    }

    db.edit_by_id(data)


    return redirect('/stock')

@app.route('/delete-item/<int:item_id>', methods=['GET'])
def delete_stock(item_id):
    
    if not checkUser():
        return redirect('/')
    
    db.remove_item(item_id)

    return redirect('/stock')


def checkUser():
    '''
    
    Checar se o usuario é permitido entrar na pagina.
    
    '''
    
    return True