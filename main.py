from app import app  # noqa: F401
from flask import request, jsonify
from firebase_admin import auth

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