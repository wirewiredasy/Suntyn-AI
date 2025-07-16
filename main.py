from app import app  # noqa: F401
from flask import render_template, request, jsonify
from config import Config
from firebase_admin import auth

@app.route('/')
def index():
    return render_template('index.html', 
                          firebase_api_key=Config.FIREBASE_API_KEY,
                          firebase_project_id=Config.FIREBASE_PROJECT_ID,
                          firebase_app_id=Config.FIREBASE_APP_ID)

@app.route("/verify-token", methods=["POST"])
def verify_token():
    try:
        data = request.get_json()
        if not data or 'token' not in data:
            return jsonify({"error": "Token is required"}), 400
            
        id_token = data["token"]
        decoded_token = auth.verify_id_token(id_token)
        
        return jsonify({
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name"),
            "picture": decoded_token.get("picture"),
            "email_verified": decoded_token.get("email_verified", False)
        })
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return jsonify({"error": str(e)}), 401