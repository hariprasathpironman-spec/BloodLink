from app.extensions import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('donor', 'hospital', 'admin', name='user_roles'), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expiry = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    donor_profile = db.relationship('Donor', backref='user', uselist=False, cascade='all, delete-orphan')
    hospital_profile = db.relationship(
        'Hospital',
        foreign_keys='Hospital.hospital_id',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )
    verified_hospitals = db.relationship(
        'Hospital',
        foreign_keys='Hospital.verified_by_admin_id',
        backref='verified_by_admin',
        lazy='dynamic'
    )
    admin_profile = db.relationship('Admin', backref='user', uselist=False, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='actor', lazy='dynamic')
