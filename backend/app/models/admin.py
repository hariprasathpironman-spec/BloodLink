from app.extensions import db

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    totp_secret = db.Column(db.String(32), nullable=True)
