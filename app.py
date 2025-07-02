from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# DB config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'restaurant.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ This MUST be in global scope
db = SQLAlchemy(app)

# ✅ Models defined AFTER db
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    room_type = db.Column(db.String(50))
    date_from = db.Column(db.String(50))
    date_to = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    food_items = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        room_type = request.form['room_type']
        date_from = request.form['date_from']
        date_to = request.form['date_to']

        booking = Booking(
            name=name,
            room_type=room_type,
            date_from=date_from,
            date_to=date_to
        )
        db.session.add(booking)
        db.session.commit()

        flash("Booking submitted successfully!", "success")
        return redirect('/book')
    return render_template('book.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        food_items = request.form.getlist('food')
        food_list = ", ".join(food_items) if food_items else "None"

        order = Order(name=name, food_items=food_list)
        db.session.add(order)
        db.session.commit()

        flash("Order placed successfully!", "success")
        return redirect('/order')
    return render_template('order.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin')
def admin_dashboard():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin.html', bookings=bookings, orders=orders)


if __name__ == '__main__':
    app.run(debug=True)

