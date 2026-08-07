from flask import Flask, send_from_directory
from app.config import Config
from app.extensions import db, jwt, mail, cors, limiter, talisman
import os

def create_app(config_class=Config):
    frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/dist'))
    app = Flask(__name__, static_folder=frontend_dist, static_url_path='/')
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configure Limiter - using in-memory for MVP, can switch to Redis for production
    limiter.init_app(app)
    
    # Talisman handles security headers like CSP. 
    # Enforcing strict CSP to prevent XSS attacks.
    csp = {
        'default-src': [
            '\'self\'',
            '*.cloudinary.com',
            '*.googleapis.com',
            '*.gstatic.com'
        ],
        'script-src': ['\'self\'', '\'unsafe-inline\''], # Allow inline for React dev build
        'style-src': ['\'self\'', '\'unsafe-inline\''],
    }
    talisman.init_app(app, content_security_policy=csp, force_https=False) # force_https=False for dev, True for Prod

    # Global Error Handlers for Security
    @app.errorhandler(400)
    def bad_request(e):
        return {"msg": "Bad Request: Invalid input detected"}, 400

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {"msg": "Rate limit exceeded. Please try again later."}, 429

    @app.errorhandler(500)
    def internal_error(e):
        return {"msg": "Internal Server Error"}, 500

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.donor import donor_bp
    from app.routes.hospital import hospital_bp
    from app.routes.request import request_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(donor_bp, url_prefix='/api/donor')
    app.register_blueprint(hospital_bp, url_prefix='/api/hospital')
    app.register_blueprint(request_bp, url_prefix='/api/request')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Register CLI commands (if any)

    @app.route('/health', methods=['GET'])
    def health_check():
        return {"status": "healthy"}, 200

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # Ensure database tables are created on startup
    with app.app_context():
        db.create_all()

    return app
