from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from datetime import datetime, timezone, timedelta
from app.extensions import db, limiter
from app.models.request import EmergencyRequest
from app.models.hospital import Hospital
from app.schemas.api import EmergencyRequestSchema
from app.utils.security import hospital_required
from app.utils.audit import log_audit_event

request_bp = Blueprint('request', __name__)

def check_fraud_flags(hospital_id, patient_name):
    """
    Checks for suspicious behavior:
    1. > 5 requests in 24 hours
    2. Duplicate patient names for active requests
    """
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)
    
    # Check frequency
    recent_requests = EmergencyRequest.query.filter(
        EmergencyRequest.hospital_id == hospital_id,
        EmergencyRequest.created_at >= yesterday
    ).count()
    
    if recent_requests >= 5:
        return True
        
    # Check duplicate patient
    duplicate = EmergencyRequest.query.filter(
        EmergencyRequest.hospital_id == hospital_id,
        EmergencyRequest.patient_name == patient_name,
        EmergencyRequest.status == 'Open'
    ).first()
    
    if duplicate:
        return True
        
    return False

@request_bp.route('/', methods=['POST'])
@jwt_required()
@hospital_required()
@limiter.limit("10 per hour")
def create_request():
    hospital_id = get_jwt_identity()
    hospital = Hospital.query.get(hospital_id)
    
    if not hospital or not hospital.verified:
        return jsonify({"msg": "Hospital not verified by admin. Cannot post requests."}), 403

    try:
        data = EmergencyRequestSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
        
    # Ensure datetime is timezone aware
    if data['required_before'].tzinfo is None:
        data['required_before'] = data['required_before'].replace(tzinfo=timezone.utc)

    # Fraud Detection
    is_suspicious = check_fraud_flags(hospital_id, data['patient_name'])

    new_request = EmergencyRequest(
        patient_name=data['patient_name'],
        blood_group=data['blood_group'],
        units_required=data['units_required'],
        urgency=data['urgency'],
        required_before=data['required_before'],
        hospital_id=hospital_id,
        flagged_suspicious=is_suspicious
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    log_audit_event(hospital_id, "EMERGENCY_REQUEST_CREATED", {
        "request_id": new_request.request_id,
        "blood_group": new_request.blood_group,
        "suspicious": is_suspicious
    })

    return jsonify({
        "msg": "Emergency request created successfully", 
        "request_id": new_request.request_id,
        "flagged": is_suspicious
    }), 201

@request_bp.route('/<int:request_id>/close', methods=['PATCH'])
@jwt_required()
@hospital_required()
def close_request(request_id):
    hospital_id = int(get_jwt_identity())
    req = EmergencyRequest.query.get(request_id)
    
    if not req:
        return jsonify({"msg": "Request not found"}), 404
        
    if req.hospital_id != hospital_id:
        return jsonify({"msg": "Unauthorized to close this request"}), 403
        
    req.status = 'Closed'
    db.session.commit()
    
    log_audit_event(hospital_id, "EMERGENCY_REQUEST_CLOSED", {"request_id": request_id})
    return jsonify({"msg": "Request closed successfully"}), 200

@request_bp.route('/', methods=['GET'])
def list_active_requests():
    """Publicly accessible list of open emergency requests"""
    requests = EmergencyRequest.query.filter_by(status='Open').order_by(EmergencyRequest.required_before.asc()).all()
    
    res = []
    for req in requests:
        res.append({
            "request_id": req.request_id,
            "patient_name": req.patient_name,
            "blood_group": req.blood_group,
            "units_required": req.units_required,
            "urgency": req.urgency,
            "required_before": req.required_before.isoformat(),
            "hospital_name": req.hospital.hospital_name,
            "district": req.hospital.district,
            "state": req.hospital.state,
            "flagged_suspicious": req.flagged_suspicious # Might hide this in production for donors
        })
        
    return jsonify(res), 200

@request_bp.route('/<int:request_id>/matches', methods=['GET'])
@jwt_required()
@hospital_required()
def get_matches(request_id):
    """
    Returns a sorted list of donors matched to this request using the AI Match Score Engine.
    Only the hospital that created the request can view its matches.
    """
    hospital_id = int(get_jwt_identity())
    req = EmergencyRequest.query.get(request_id)
    
    if not req:
        return jsonify({"msg": "Request not found"}), 404
        
    if req.hospital_id != hospital_id:
        return jsonify({"msg": "Unauthorized to view matches for this request"}), 403

    # Add the hospital's location data to the request object for matching calculation
    req.district = req.hospital.district
    req.state = req.hospital.state

    from app.models.donor import Donor
    from app.utils.matching import calculate_match_score

    # Fetch all donors (in production, we might filter by state/blood group to optimize)
    # For MVP, we'll fetch all active donors and score them
    donors = Donor.query.all()
    
    matches = []
    for donor in donors:
        # Don't suggest donors who aren't verified or available if required
        if not donor.user.verified:
            continue
            
        match_result = calculate_match_score(donor, req)
        # Filter out completely incompatible donors if score is too low, or just return them sorted
        # We will return everyone but sorted by score
        
        matches.append({
            "donor_id": donor.donor_id,
            "name": donor.user.name,
            "blood_group": donor.blood_group,
            "district": donor.district,
            "state": donor.state,
            "age": donor.age,
            "score": match_result['score'],
            "badge": match_result['badge'],
            "last_donation": donor.last_donation.isoformat() if donor.last_donation else None,
            "profile_image_url": donor.profile_image_url
        })
        
    # Sort descending by score
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    # Optional: Log the match query for audit (could be too noisy, skipped for now)

    return jsonify(matches), 200
