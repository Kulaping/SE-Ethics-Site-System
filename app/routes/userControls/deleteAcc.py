from flask import (Blueprint, request, jsonify)
from app.models.models import db, Userdb
from sqlalchemy import delete
from app.logger.logger import log_info

delete = Blueprint("deleteAcc", __name__)

@delete.route("/deleteAcc", methods=["POST"])
def remove():
      
      message = request.get_json()
      confirm = message.get("confirm_delete") 
      userName = message.get("userID")
      
      user_to_delete = Userdb.query.filter_by(username=userName).first()
      
      if confirm is True:
            log_info(confirm)
           # log_info(f"{userName} on: {user_to_delete}")
            db.session.delete(user_to_delete)
            db.session.commit()
            log_info("Deleted")
                  
      else:
          status = "Aborted"
          log_info(status)
             
          return jsonify({
                "confirm": False, 
                "message": status
                })
             
      
      return jsonify({"res": confirm})

    
'''
    try:
        
       if confirmation is True:
          print(confirmation)
          
    except ValueError as e:
           print(e)
''' 