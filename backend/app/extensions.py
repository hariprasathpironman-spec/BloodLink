from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

# Initialize extensions (they will be bound to the app in create_app())
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
cors = CORS()

# Setup rate limiter using the client's IP address
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Talisman for setting HTTP security headers
talisman = Talisman()
