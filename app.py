from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import random
from bson.objectid import ObjectId

app = Flask("Products")
app.config['MONGO_URI'] = "mongodb://localhost:27017/Products-db"

Bootstrap(app)

mongo = PyMongo(app)

app.config['SECRET_KEY'] = 'sOmE_rAnDom_woRd'
@app.route('/', methods=['GET', 'POST'])
def shop_route():
    if request.method == 'GET':
        return render_template('one-stop-shop.html')
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        doc = {}
        for item in request.form:
            doc[item] = request.form[item]
        print(doc)
        mongo.db.products.insert_one(doc)
        return redirect('/')
@app.route('/buy', methods=['GET', 'POST'])
def buy():
    if request.method == 'GET':
        session['cart-items'] = {}
        found_products = mongo.db.products.find()
        return render_template('buy.html', products=found_products)
    elif request.method == 'POST':
        doc = {}
        print(request.form)
        for item in request.form:
            if int(request.form[item]) != 0:
                doc[item] = request.form[item]
        session['cart-items'] = doc
        print(doc)
        return redirect('/checkout')
@app.route('/checkout')
def checkout():
    total = 0
    cart_items=[]
    stored_info = session['cart-items']

    for ID in stored_info:
        print(ID)
        found_item = mongo.db.products.find_one({'_id': ObjectId(ID)})
        found_item['bought'] = stored_info[ID]
        found_item['item-total'] = int(found_item['Price']) * int(found_item['bought'])
        cart_items.append(found_item)
        total += found_item['item-total']
    return render_template('checkout.html', products=cart_items, total=total)

app.run(debug=True)