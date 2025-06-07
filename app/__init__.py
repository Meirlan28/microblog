#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from prometheus_flask_exporter import PrometheusMetrics 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

        
    app.config.from_object(Config)
    app.config['DEBUG'] = True

    db.init_app(app)

    metrics = PrometheusMetrics(app)

    metrics.info('app_info', 'Application info', version='1.0.0')


    with app.app_context():
        from . import routes, models
        app.register_blueprint(routes.bp)
        db.create_all()

    return app