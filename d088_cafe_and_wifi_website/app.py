from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask app
app = Flask(__name__)

# Absolute path to cafes.db file (ensure it's in the same folder as app.py)
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cafes.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'  # Use absolute path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Cafe model (without rating and is_favorite)
class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    map_url = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=True)
    coffee_price = db.Column(db.String(250), nullable=True)

# Home route to display all cafes
@app.route('/')
def index():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)

# Add cafe route
@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        map_url = request.form['map_url']
        img_url = request.form['img_url']
        has_wifi = 'has_wifi' in request.form
        has_sockets = 'has_sockets' in request.form
        has_toilet = 'has_toilet' in request.form
        can_take_calls = 'can_take_calls' in request.form
        seats = request.form['seats']
        coffee_price = request.form['coffee_price']

        new_cafe = Cafe(
            name=name,
            location=location,
            map_url=map_url,
            img_url=img_url,
            has_wifi=has_wifi,
            has_sockets=has_sockets,
            has_toilet=has_toilet,
            can_take_calls=can_take_calls,
            seats=seats,
            coffee_price=coffee_price
        )

        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')  # Render the add cafe form

# Delete cafe route
@app.route('/delete/<int:id>', methods=['GET'])
def delete_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    db.session.delete(cafe)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
