
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Import and register blueprints
from routes.main import main_bp
from routes.tools import tools_bp
from routes.auth import auth_bp

app.register_blueprint(main_bp)
app.register_blueprint(tools_bp, url_prefix='/tools')
app.register_blueprint(auth_bp, url_prefix='/auth')

# Global error handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
