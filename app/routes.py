from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app import db
from app.models import Animal

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    animals = Animal.query.all()
    return render_template('index.html', animals=animals)

@bp.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        new_animal = Animal(name=name, species=species)
        db.session.add(new_animal)
        db.session.commit()
        return redirect(url_for('main.index'))  # Перенаправляем на главную страницу
    return render_template('add_animal.html')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    return redirect(url_for('main.index'))
