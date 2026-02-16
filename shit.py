from app import create_app
   
app = create_app()

print("Template folder:", app.template_folder)

#load_dotenv()

if __name__ == "__main__":
    app.run(debug=True)