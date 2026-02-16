from flask import Blueprint, request, jsonify, session
import json
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import db, Userdb #comments
from app.services.jwt_service import token, decode
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
    return jsonify({"ok": True, "token": auth, "username": user.username})


# Login
@auth_bp.route("/log-in_logic", methods=["POST"])
def login_auth():
    username, password = credentials()
    user = Userdb.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        auth = token(user)
        return jsonify({"ok": True, "token": auth, "username": user.username})
    else:
        return jsonify({"ok": False, "error_log": "Invalid credentials"})

# Acc auth
@auth_bp.route("/accounts", methods=["GET"])
def show_acc():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"ok": False, "error": "No Token"}), 401

    try:
        actual_token = auth_header.split(" ")[1]
        payload = decode(actual_token)
        return jsonify({"username": payload["username"], "ok": True})
    except Exception:
        return jsonify({"ok": False, "error": "Invalid or expired token"}), 401
