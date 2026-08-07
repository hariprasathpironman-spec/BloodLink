from app.extensions import db
from datetime import datetime, timezone

class EmergencyRequest(db.Model):
    __tablename__ = 'emergency_requests'
    
    request_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False, index=True)
    units_required = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.Enum('High', 'Medium', 'Low', name='urgency_levels'), nullable=False)
    required_before = db.Column(db.DateTime, nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'), nullable=False)
    status = db.Column(db.Enum('Open', 'Fulfilled', 'Closed', name='request_status'), default='Open', nullable=False)
    flagged_suspicious = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    donations = db.relationship('Donation', backref='emergency_request', lazy='dynamic')
