from src.shared import Shared

db = Shared.db


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
