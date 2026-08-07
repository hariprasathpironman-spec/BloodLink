import json
import hashlib
from app.extensions import db
from app.models.audit_log import AuditLog

def verify_audit_chain() -> bool:
    """
    Validates the cryptographic hash chain of the Audit Log.
    Returns True if the chain is intact, False if tampering is detected.
    """
    logs = AuditLog.query.order_by(AuditLog.id.asc()).all()
    
    if not logs:
        return True # Empty log is valid
        
    expected_previous_hash = "0" * 64
    
    for idx, log in enumerate(logs):
        if log.previous_hash != expected_previous_hash:
            print(f"❌ TAMPERING DETECTED at Log ID {log.id}: Invalid previous hash.")
            return False
            
        # Re-calculate hash
        # Hash calculation: SHA256(previous_hash + action + actor_id + event_data_json)
        # Note: Must dump json identically (sort_keys=True)
        event_data_json = json.dumps(log.event_data_json, sort_keys=True)
        hash_input = f"{log.previous_hash}{log.action}{log.actor_id}{event_data_json}"
        calculated_hash = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
        
        if calculated_hash != log.current_hash:
            print(f"❌ TAMPERING DETECTED at Log ID {log.id}: Data payload altered!")
            return False
            
        expected_previous_hash = log.current_hash
        
    print(f"✅ Audit Log Cryptographic Chain Validated: {len(logs)} records securely verified.")
    return True

if __name__ == "__main__":
    # This block allows running verification as a standalone script using the Flask App Context
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from app import create_app
    
    app = create_app()
    with app.app_context():
        is_valid = verify_audit_chain()
        if not is_valid:
            sys.exit(1)
        sys.exit(0)
