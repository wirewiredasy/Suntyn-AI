from app import app  # noqa: F401
# No authentication required - all tools are freely accessible

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(tools_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

# Register enhanced API
try:
    from routes.enhanced_tool_api import enhanced_api_bp
    app.register_blueprint(enhanced_api_bp)
    print("✅ Enhanced API v2 registered successfully")
except Exception as e:
    print(f"⚠️ Enhanced API registration failed: {e}")