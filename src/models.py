from . import db


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(200), default="0/")
    name = db.Column(db.String(50), nullable=False)
    processed = db.Column(db.Boolean, default=False)
    result = db.Column(db.Integer)
