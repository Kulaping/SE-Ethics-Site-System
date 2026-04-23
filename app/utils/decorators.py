from functools import wraps
from flask import request, jsonify
from app.services.jwt_service import decode
from app.logger.logger import log_info

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        userID = None
        
        if auth_header:       
            try:
                actual_token = auth_header.split(" ")[1]
                payload = decode(actual_token)
                userID = payload["user-id"]
            except Exception:
                   log_info("Invalid or expired token"), 401

        return f(userID, *args, **kwargs)

    return decorated