from flask import Blueprint, jsonify
from app.models.models import Userdb
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

users = Blueprint("users", __name__)

@users.route("/get_users", methods=["GET"])
def get_users():
    users = Userdb.query.all()
    for user in users:
        logger.info("User:", user.username, "Hashed PW:", user.password)
    
    usernames = [user.username for user in users]
    passwords = [psw.password for psw in users]
    return jsonify({"status": True, "users": usernames, "password": passwords})