from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)

users, orders, offers = load_json('users.json'), load_json('orders.json'), load_json('offers.json')


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


with app.app_context():
    db.drop_all()
    db.create_all()

    for line in users:
        l = User(**line)
        db.session.add(l)
        db.session.commit()

    for line in orders:
        l = Order(**line)
        db.session.add(l)
        db.session.commit()

    for line in offers:
        l = Offer(**line)
        db.session.add(l)
        db.session.commit()


@app.route('/')
def main_page():
    return 'Главная страница'


# данные выводятся не в том порядке, что в json
@app.route('/users', methods=['GET', 'POST'])
def users_page():
    if request.method == 'GET':
        users = User.query.all()
        users_list = []
        for user in users:
            users_list.append(to_dict(user))
        return jsonify(users_list)

    elif request.method == 'POST':
        user_data = request.json
        db.session.add(User(**user_data))
        db.session.commit()
        return '', 201



@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def user_page(uid):
    if request.method == 'GET':
        user = User.query.get(uid)
        return jsonify(to_dict(user))

    elif request.method == 'PUT':
        user = User.query.get(uid)

        user.id = users['id']
        user.first_name = users['first_name']
        user.last_name = users['last_name']
        user.age = user['age']
        user.email = user['email']
        user.role = user['role']
        user.phone = user['phone']

        db.session.add(user)
        db.session.commit()

        return '', 202


    elif request.method == 'DELETE':
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return '', 202


@app.route('/orders', methods = ['GET', 'POST'])
def orders_all():
    if request.method == 'GET':
        orders = Order.query.all()
        result = []
        for order in orders:
            result.append(to_dict(order))
        return jsonify(result)

    elif request.method == 'POST':
        orders = request.json
        db.session.add(Order(**orders))
        db.session.commit()
        return '', 201


@app.route('/orders/<int:uid>', methods = ['GET', 'PUT', 'DELETE'])
def order_by_id(uid):
    if request.method == 'GET':
        order = Order.query.get(uid)
        return jsonify(to_dict(order))

    elif request.method == 'PUT':
        order = Order.query.get(uid)

        order.id = orders['id']
        order.name = orders['name']
        order.description = orders['description']
        order.start_date = orders['start_date']
        order.end_date = orders['end_date']
        order.address = orders['address']
        order.price = orders['price']
        order.customer_id = orders['customer_id']
        order.executor_id = orders['executor_id']

        db.session.add(order)
        db.session.commit()

        return '', 202


    elif request.method == 'DELETE':
        order = Order.query.get(uid)
        db.session.delete(order)
        db.session.commit()
        return '', 202


@app.route('/offers', methods = ['GET', 'POST'])
def offers_all():
    if request.method == 'GET':
        offers = Offer.query.all()
        result = []
        for offer in offers:
            result.append(to_dict(offer))
        return jsonify(result)

    elif request.method == 'POST':
        offers = request.json
        db.session.add(Order(**offers))
        db.session.commit()
        return '', 201


@app.route('/offers/<int:uid>', methods = ['GET', 'PUT', 'DELETE'])
def offer_by_id(uid):
    if request.method == 'GET':
        offer = Offer.query.get(uid)
        return jsonify(to_dict(offer))

    elif request.method == 'PUT':
        offer = Order.query.get(uid)

        offer.id = offers['id']
        offer.order_id = offers['order_id']
        offer.executor_id = offers['executor_id']

        db.session.add(offer)
        db.session.commit()

        return '', 202


    elif request.method == 'DELETE':
        order = Order.query.get(uid)
        db.session.delete(order)
        db.session.commit()
        return '', 202


if __name__ == "__main__":
    app.run(debug=True)
