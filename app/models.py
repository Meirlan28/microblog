#models.py
from app import db

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    species = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Animal {self.name}>'
