from app.extensions import db

class Hospital(db.Model):
    __tablename__ = 'hospitals'
    
    hospital_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    hospital_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text, nullable=False)
    district = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False, index=True)
    contact = db.Column(db.String(20), nullable=False)
    verification_doc_url = db.Column(db.String(255), nullable=True)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    verified_by_admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relationships
    emergency_requests = db.relationship('EmergencyRequest', backref='hospital', lazy='dynamic', cascade='all, delete-orphan')
