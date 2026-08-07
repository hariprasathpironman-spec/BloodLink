from app.extensions import db

class Donor(db.Model):
    __tablename__ = 'donors'
    
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    blood_group = db.Column(db.String(5), nullable=False, index=True)
    district = db.Column(db.String(100), nullable=False, index=True)
    state = db.Column(db.String(100), nullable=False, index=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    last_donation = db.Column(db.Date, nullable=True)
    availability = db.Column(db.Boolean, default=True, nullable=False)
    profile_image_url = db.Column(db.String(255), nullable=True)

    # Relationships
    donations = db.relationship('Donation', backref='donor', lazy='dynamic')
