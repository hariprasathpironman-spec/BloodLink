from app.extensions import db
from datetime import datetime, timezone
import json

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action = db.Column(db.String(255), nullable=False)
    event_data_json = db.Column(db.JSON, nullable=False)
    previous_hash = db.Column(db.String(64), nullable=False)
    current_hash = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    @staticmethod
    def get_last_hash():
        last_log = AuditLog.query.order_by(AuditLog.id.desc()).first()
        if last_log:
            return last_log.current_hash
        return "0" * 64  # Genesis hash
