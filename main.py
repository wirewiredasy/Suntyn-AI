from app import app  # noqa: F401
from flask import render_template
from config import Config

@app.route('/')
def index():
    return render_template('index.html', 
                          firebase_api_key=Config.FIREBASE_API_KEY,
                          firebase_project_id=Config.FIREBASE_PROJECT_ID,
                          firebase_app_id=Config.FIREBASE_APP_ID)