from config import *
import estoque_db


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

    estoque_db.add_to_stock(name, quantity, price, category, description)

    return redirect("/stock")

@app.route("/stock")
def stock_view():

    if not checkUser():
        return redirect('/')

    data = estoque_db.fetch_data_dic()
    print(data)

    return render_template("stock.html", data=data)
    

@app.route("/edit_stock/<int:item_id>", methods=['GET'])
def editar_item(item_id):
    
    if not checkUser():
        return redirect('/')

    data = estoque_db.fetch_data_by_id(item_id)
    data = estoque_db.item_to_dic(data)

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

    estoque_db.edit_by_id(data)


    return redirect('/stock')

@app.route('/delete-item/<int:item_id>', methods=['GET'])
def delete_stock(item_id):
    
    if not checkUser():
        return redirect('/')
    
    estoque_db.remove_item(item_id)

    return redirect('/stock')


def checkUser():
    '''
    
    Checar se o usuario é permitido entrar na pagina.
    
    '''
    
    return True

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
