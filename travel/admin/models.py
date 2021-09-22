from travel import db
from sqlalchemy.sql import func

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return '<Admin %r>' % self.name