from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/stock_add")
def stock_add_page():
    return render_template('stock_add.html')

@app.route("/submit-stock", methods=['POST'])
def submit_stock():
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

    return redirect("/")

@app.route("/stock")
def stock_view():
    data = db.fetch_data_dic()
    return render_template("stock.html", data=data)

@app.route("/editar_item/<int:item_id>")
def editar_item(item_id):
    return render_template("index.html")