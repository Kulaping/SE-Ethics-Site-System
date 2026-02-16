from flask import request
import re

def credentials():
    data = request.get_json()
    return data.get("username"), data.get("password")

#TODO: Should rename the file name, or just put this 
# comment function into an another file or in my sumbit_comment.py
def comment():
    try:
       data = request.get_json()
       
       if data.get("comment") == "":
          return
       
       else:    
          return data.get("comment"), data.get("specific_article")
   
    except Exception as e:
       print(str(e))
       print("failed")
    
def validate_username(username):
    USERNAME_REGEX = r"^[A-Za-z0-9_@-]{4,17}$"
    return bool(re.match(USERNAME_REGEX, username))

def validate_password(password):
    PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
    return bool(re.match(PASSWORD_REGEX, password))