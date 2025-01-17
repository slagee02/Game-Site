from uuid import _uuid
from __init__ import db, app


class User(db.Model):
    __tablename__ = "users" #for table name
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(20), unique = True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    password = db.Column(db.String(30), nullable=False) #limit bycrypt password hash 30


#db.drop_all()
#with app.app_context():
    #db.create_all()
