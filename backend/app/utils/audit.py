import json
import hashlib
from datetime import datetime, timezone
from app.extensions import db
from app.models.audit_log import AuditLog

def log_audit_event(actor_id: int, action: str, event_data: dict):
    """
    Secure append-only audit log with a cryptographic hash chain.
    """
    previous_hash = AuditLog.get_last_hash()
    event_data_json = json.dumps(event_data, sort_keys=True)
    
    # Hash calculation: SHA256(previous_hash + action + actor_id + event_data_json)
    hash_input = f"{previous_hash}{action}{actor_id}{event_data_json}"
    current_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    
    log_entry = AuditLog(
        actor_id=actor_id,
        action=action,
        event_data_json=event_data,
        previous_hash=previous_hash,
        current_hash=current_hash,
        timestamp=datetime.now(timezone.utc)
    )
    
    db.session.add(log_entry)
    db.session.commit()
