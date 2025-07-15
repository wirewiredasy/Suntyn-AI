from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Import blueprints here (e.g., from .main import main_bp)
# Example:
# from .main import main_bp
# from .tools import tools_bp
# from .api import api_bp
# from .auth import auth_bp
# app.register_blueprint(main_bp)


def create_app():
    # Initialize Flask app

    # Example Blueprint registration
    # from .main import main_bp
    # from .tools import tools_bp
    # from .api import api_bp
    # from .auth import auth_bp
    # Register blueprints
    # app.register_blueprint(main_bp)
    # app.register_blueprint(tools_bp, url_prefix='/tools')
    # app.register_blueprint(api_bp, url_prefix='/api')
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    # Global error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app