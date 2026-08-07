from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from app.models.hospital import Hospital
from app.schemas.api import UpdateHospitalSchema
from app.utils.security import hospital_required
from app.utils.audit import log_audit_event

hospital_bp = Blueprint('hospital', __name__)

@hospital_bp.route('/profile', methods=['GET'])
@jwt_required()
@hospital_required()
def get_profile():
    user_id = get_jwt_identity()
    hospital = Hospital.query.get(user_id)
    if not hospital:
        return jsonify({"msg": "Hospital profile not found"}), 404
        
    return jsonify({
        "hospital_name": hospital.hospital_name,
        "email": hospital.user.email,
        "address": hospital.address,
        "district": hospital.district,
        "state": hospital.state,
        "contact": hospital.contact,
        "verified": hospital.verified,
        "verification_doc_url": hospital.verification_doc_url
    }), 200

@hospital_bp.route('/profile', methods=['PUT'])
@jwt_required()
@hospital_required()
def update_profile():
    user_id = get_jwt_identity()
    hospital = Hospital.query.get(user_id)
    if not hospital:
        return jsonify({"msg": "Hospital profile not found"}), 404

    try:
        data = UpdateHospitalSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        setattr(hospital, key, value)
        
    db.session.commit()
    log_audit_event(user_id, "HOSPITAL_PROFILE_UPDATED", {"updated_fields": list(data.keys())})
    
    return jsonify({"msg": "Profile updated successfully"}), 200
