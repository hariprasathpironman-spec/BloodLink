from flask import Flask, send_from_directory, jsonify
from app.config import Config
from app.extensions import db, jwt, mail, cors, limiter, talisman
import os
import traceback

FRONTEND_DIST = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../frontend/dist')
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    limiter.init_app(app)

    csp = {
        'default-src': ['\'self\'', '*.cloudinary.com', '*.googleapis.com', '*.gstatic.com'],
        'script-src': ['\'self\'', '\'unsafe-inline\''],
        'style-src':  ['\'self\'', '\'unsafe-inline\''],
    }
    talisman.init_app(app, content_security_policy=csp, force_https=False)

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(msg="Bad Request: Invalid input detected"), 400

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify(msg="Rate limit exceeded. Please try again later."), 429

    # Catch ALL exceptions so we don't get Gunicorn's HTML page
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Pass through HTTP errors
        if hasattr(e, 'code') and isinstance(e.code, int):
            return jsonify(msg=str(e)), e.code
        
        # Log the full traceback to Railway logs
        app.logger.error(f"Unhandled Exception: {str(e)}")
        app.logger.error(traceback.format_exc())
        
        # Return the actual error message to the frontend so we can see what crashed!
        return jsonify(msg=f"Server Crash: {str(e)}"), 500

    from app.routes.auth     import auth_bp
    from app.routes.donor    import donor_bp
    from app.routes.hospital import hospital_bp
    from app.routes.request  import request_bp
    from app.routes.admin    import admin_bp

    app.register_blueprint(auth_bp,      url_prefix='/api/auth')
    app.register_blueprint(donor_bp,     url_prefix='/api/donor')
    app.register_blueprint(hospital_bp,  url_prefix='/api/hospital')
    app.register_blueprint(request_bp,   url_prefix='/api/request')
    app.register_blueprint(admin_bp,     url_prefix='/api/admin')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify(status="healthy"), 200

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        file_path = os.path.join(FRONTEND_DIST, path)
        if path and os.path.isfile(file_path):
            return send_from_directory(FRONTEND_DIST, path)
        return send_from_directory(FRONTEND_DIST, 'index.html')

    with app.app_context():
        db.create_all()

    return app
