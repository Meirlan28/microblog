import logging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, abort
from app import db
from app.models import Animal
import time
from pythonjsonlogger import jsonlogger
from datetime import datetime

bp = Blueprint('main', __name__)

# Настройка логгера с JSON форматером
logger = logging.getLogger('myapp')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(host)s %(user_identifier)s %(datetime)s %(method)s %(request)s %(protocol)s %(status)s %(bytes)s %(referer)s %(message)s'
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_log_data(status=200, bytes_=0, message="Request processed"):
    return {
        "host": request.remote_addr or "",
        "user_identifier": "anonymous",  # если есть авторизация — подставь сюда
        "datetime": datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S +0000"),
        "method": request.method,
        "request": request.path,
        "protocol": request.environ.get('SERVER_PROTOCOL'),
        "status": status,
        "bytes": bytes_,
        "referer": request.referrer or "",
        "log_message": message
    }

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
        logger.info("", extra=get_log_data(message=f"Added animal: Name={name}, Species={species}"))
        return redirect(url_for('main.index'))
    return render_template('add_animal.html')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    
    # Логируем информацию об удалении
    logger.info("", extra=get_log_data(message=f"Deleted animal: ID={animal.id}, Name={animal.name}, Species={animal.species}"))
    
    db.session.delete(animal)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/status/<int:code>')
def error_simulator(code):
    seconds_sleep = request.args.get('seconds_sleep', default=0, type=float)
    if seconds_sleep > 0:
        time.sleep(seconds_sleep)  # Задержка
    
    if code in [400, 403, 404, 409, 500]:
        logger.info("", extra=get_log_data(status=code, message=f"Simulated error {code}"))
        abort(code)
    return f"Unsupported code: {code}", 400
