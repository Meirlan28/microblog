import logging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, abort
from app import db
from app.models import Animal
import time

bp = Blueprint('main', __name__)

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Можно настроить обработчик, чтобы выводить в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


@bp.route('/')
def index():
    animals = Animal.query.limit(10).all()
    return render_template('index.html', animals=animals)

@bp.route('/add_animal', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        new_animal = Animal(name=name, species=species)
        db.session.add(new_animal)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_animal.html')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    
    # Логируем информацию об удалении
    logger.info(f"User IP {request.remote_addr} deleted animal: ID={animal.id}, Name={animal.name}, Species={animal.species}")
    
    db.session.delete(animal)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/status/<int:code>')
def error_simulator(code):
    seconds_sleep = request.args.get('seconds_sleep', default=0, type=float)
    if seconds_sleep > 0:
        time.sleep(seconds_sleep)  # Задержка
    
    if code in [400, 403, 404, 409, 500]:
        abort(code)
    return f"Unsupported code: {code}", 400
