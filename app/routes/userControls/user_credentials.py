from flask import Blueprint, jsonify
from app.services.userpreference.preference import Prefencemanager
from app.logger.logger import log_info
from app.utils.decorators import token_required

credentials = Blueprint("user_credentials", __name__)

@credentials.route("/user_info", methods=["GET"])
@token_required
def user_credentials(userID): 
    log_info("If this shit prints, this function gets executed")
    log_info(f"user ID for user creds file: {userID}")
    user_manager = Prefencemanager(userID) 
    
    max_cat = user_manager.get_highest_cat()
    log_info(f"returned category: {max_cat}")
    
    return jsonify({"preferred_category": max_cat})