from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__, template_folder="../templates")

@pages_bp.route('/main')
def main():
   return render_template("a.html")

@pages_bp.route('/dash')
def sec():
   return render_template('Dashboard.html')

@pages_bp.route('/click') 
def news():
    return render_template('news.html')
 
@pages_bp.route('/register') 
def register():
    return render_template('register.html') 
 
@pages_bp.route('/log-in') 
def renderLog_page():
    return render_template('login.html') 

@pages_bp.route('/testing') 
def test_page():
    return render_template('tet.html') 

@pages_bp.route("/list-templates")
def list_templates():
    import os
    return str(os.listdir("templates"))

@pages_bp.route("/jinja-test")
def jinja_test():
    from flask import current_app
    return str(current_app.jinja_env.list_templates())

@pages_bp.route("/static-check")
def static_check():
    import os
    return str(os.listdir("static/javascript"))