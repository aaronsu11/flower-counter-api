from . import db


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    batchid = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(200), default="0/")
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="uploaded")
    result = db.Column(db.Integer)
