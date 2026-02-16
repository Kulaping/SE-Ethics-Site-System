import jwt 
from flask import current_app
from datetime import (datetime, timedelta, UTC)

def token(user):
    payload = { 
          "username": user.username,
          "user-id": user.id,
          "exp": datetime.now(UTC) + timedelta(hours=1)           
    } 
    print(payload["exp"])
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def decode(token):
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])