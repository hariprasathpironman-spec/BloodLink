from app.extensions import db
from datetime import datetime, timezone

class Donation(db.Model):
    __tablename__ = 'donations'
    
    donation_id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.donor_id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('emergency_requests.request_id'), nullable=False)
    donated_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
