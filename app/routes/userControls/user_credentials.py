from flask import Blueprint, jsonify, request
from app.services.userpreference.preference import Prefencemanager
from app.logger.logger import log_info
from app.utils.decorators import token_required
from app.services.jwt_service import token, decode

credentials = Blueprint("user_credentials", __name__)

@credentials.route("/user_info", methods=["GET"])
#@token_required
def user_credentials(): 
    log_info("If this shit prints, this function gets executed")
    auth_cookie = request.cookies.get("access_token")
    if not auth_cookie:
        return jsonify({"ok": False, "error": "No Token"}), 401
    
    try:
        
       payload = decode(auth_cookie) 
       userID = payload["user-id"]
       username = payload["username"]
       log_info(f"user ID for user creds file: {userID}")
       user_manager = Prefencemanager(userID) 
    
       max_cat = user_manager.get_highest_cat()
       log_info(f"returned category: {max_cat}")
       return jsonify({"ok": True, "username": username, "fav_cat": max_cat})
    
    except Exception:
          return jsonify(
          {"ok": False, "error": "Invalid or expired token"}), 401

    
    
    
   
   
   
