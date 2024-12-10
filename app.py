from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return '<Product%r' % self.name

with app.app_context():
    db.create_all()


@app.route('/')
def hello():
    return "Witaj w aplikacji Flask z SQLAlchemy!"

#Dodawanie produktu
@app.route('/add_product/<name>/<price>')
def add_product(name, price):
    new_product = Product(name=name, price=price)
    db.session.add(new_product)
    db.session.commit()
    return f'Produkt {name} został dodany.'

#Wyświetlenie wszystkich produktów
@app.route('/products')
def products():
    products = Product.query.all()
    products_list = [f"{product.id}: {product.name} {product.price}" for product in products]
    return "<br>".join(products_list)


#Dodanie użytkownika 
@app.route('/add_user/<username>/<email>')
def add_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return f'Użytkownik {username} został dodany.'


#Usuwanie użytkownika 
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user_to_delete = User.query.get(user_id)
    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return f'Użytkownik o ID {user_id} został usunięty.'
    else:
        return f'Użytkownik o ID {user_id} nie istnieje.'

#Wyświetlanie użytkowników
@app.route('/users')
def users():
    users = User.query.all()
    users_list = [f"{user.id}: {user.username} {user.email}" for user in users]
    return "<br>".join(users_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
