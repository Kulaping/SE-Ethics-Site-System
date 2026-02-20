#from sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update, delete
from datetime import datetime, UTC


db = SQLAlchemy()

class Userdb(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(50), nullable=False)
      password = db.Column(db.String(100), nullable=False)
      comments = db.relationship(
            "comments", 
            backref="author", 
            lazy=True, 
            cascade="all, delete-orphan"
            )
 
class comments(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      user_id = db.Column(db.Integer, db.ForeignKey('userdb.id'), nullable=False)
      user_comments = db.Column(db.String(1000), nullable=False)
      timestamp = db.Column(db.DateTime, default=datetime.now(UTC))
      #article = db.column() 
      article_url = db.Column(db.String(500), index=True)
      
''' 
def wipe_user_credentials():
    db.session.execute(delete(Userdb))
    db.session.execute(delete(comments))
    db.session.commit()
'''     
