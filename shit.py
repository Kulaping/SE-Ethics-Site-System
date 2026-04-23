from app import create_app
#from app.models import Userdb, comments, userPreference

   
app = create_app()

print("Template folder:", app.template_folder)

#load_dotenv()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)