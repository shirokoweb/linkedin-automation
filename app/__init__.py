from flask import Flask
from config.jelastic import JelasticConfig
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(JelasticConfig)
    app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Register blueprints
    from app.routes import api_bp
    from app.oauth import oauth_bp
    from app.monitoring import monitor_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(oauth_bp)
    app.register_blueprint(monitor_bp)
    
    return app
