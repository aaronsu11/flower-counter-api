from . import db


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(50), nullable=False)
    batchid = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(200), default="0/", nullable=False)
    vineyard = db.Column(db.String(50), nullable=False)
    block = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    variety = db.Column(db.String(50), nullable=False)
    el_stage = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), default="uploaded")
    result = db.Column(db.Numeric)
    estimate = db.Column(db.Numeric)


class Parameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)
    slope = db.Column(db.Numeric, nullable=False)
    intercept = db.Column(db.Numeric, nullable=False)
