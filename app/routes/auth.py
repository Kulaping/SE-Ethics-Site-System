from flask import (Blueprint, request, jsonify, session, make_response)
import json
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import db, Userdb #comments
from app.services.jwt_service import token, decode
from app.routes.news import get_news
from app.logger.logger import log_info
from app.services.auth_service import (
    credentials,
   # comment,
    validate_username,
    validate_password,
)

auth_bp = Blueprint("auth", __name__)

#  Register
@auth_bp.route("/register_logic", methods=["POST"])
def register_auth():
    username, password = credentials()

    if not validate_username(username) and not validate_password(password):
        return jsonify({"ok": False, "log": "Invalid format."})

    if not validate_username(username):
        return jsonify({"ok": False, "log": "Invalid username format."})

    if not validate_password(password):
        return jsonify({"ok": False, "log": "Invalid password format."})

    if Userdb.query.filter_by(username=username).first():
        return (
            jsonify(
                {
                    "ok": False,
                    "user-inputLine": False,
                    "log": "Username/Account already exists",
                }
            ),
            400,
        )
    
    user = Userdb(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    auth = token(user)

    response = make_response(jsonify({"ok": True, "username": user.username}))
    response.set_cookie(
            "access_token", auth, httponly=True, samesite="Strict"
    )
    log_info(f"cookie res: {response}")
    log_info(f"Username test: {response.json['username']}") 
    return response
    
# Login
@auth_bp.route("/log-in_logic", methods=["POST"])
def login_auth():
    username, password = credentials()
    user = Userdb.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        auth = token(user)
        
        response = make_response(jsonify({"ok": True, "username": user.username}))
        response.set_cookie(
            "access_token", auth, httponly=True, samesite="Strict"
        )
        log_info(f"cookie res: {response}")
        log_info(f"Username test: {response.json['username']}") 
        return response
    else:
        return jsonify({"ok": False, "error_log": "Invalid credentials"})

# Acc auth
@auth_bp.route("/accounts", methods=["GET"])
def show_acc():
    #auth_header = request.headers.get("Authorization")
    auth_cookie = request.cookies.get("access_token")
   
    if not auth_cookie:
        return jsonify({"ok": False, "error": "No Token"}), 401
    
    try:
       payload = decode(auth_cookie)
       log_info(f"Decoded payload: {payload}")
       user_id = payload["username"]
       log_info(f"if it's not empty: {user_id}")
       
       return jsonify({"ok": True, "username": user_id})
        
    except Exception:
          return jsonify(
          {"ok": False, "error": "Invalid or expired token"}), 401