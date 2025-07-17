from app import app  # noqa: F401

# Register enhanced API
try:
    from routes.enhanced_tool_api import enhanced_api_bp
    app.register_blueprint(enhanced_api_bp)
    print("✅ Enhanced API v2 registered successfully")
except Exception as e:
    print(f"⚠️ Enhanced API registration failed: {e}")