from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from app.models.donor import Donor
from app.schemas.api import UpdateDonorSchema
from app.utils.security import donor_required
from app.utils.audit import log_audit_event

donor_bp = Blueprint('donor', __name__)

@donor_bp.route('/profile', methods=['GET'])
@jwt_required()
@donor_required()
def get_profile():
    user_id = get_jwt_identity()
    donor = Donor.query.get(user_id)
    if not donor:
        return jsonify({"msg": "Donor profile not found"}), 404
        
    return jsonify({
        "name": donor.user.name,
        "email": donor.user.email,
        "blood_group": donor.blood_group,
        "district": donor.district,
        "state": donor.state,
        "age": donor.age,
        "gender": donor.gender,
        "weight": donor.weight,
        "last_donation": donor.last_donation.isoformat() if donor.last_donation else None,
        "availability": donor.availability,
        "profile_image_url": donor.profile_image_url
    }), 200

@donor_bp.route('/profile', methods=['PUT'])
@jwt_required()
@donor_required()
def update_profile():
    user_id = get_jwt_identity()
    donor = Donor.query.get(user_id)
    if not donor:
        return jsonify({"msg": "Donor profile not found"}), 404

    try:
        data = UpdateDonorSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        setattr(donor, key, value)
        
    db.session.commit()
    log_audit_event(user_id, "DONOR_PROFILE_UPDATED", {"updated_fields": list(data.keys())})
    
    return jsonify({"msg": "Profile updated successfully"}), 200

@donor_bp.route('/availability', methods=['PATCH'])
@jwt_required()
@donor_required()
def toggle_availability():
    user_id = get_jwt_identity()
    donor = Donor.query.get(user_id)
    if not donor:
        return jsonify({"msg": "Donor profile not found"}), 404

    is_available = request.json.get('availability')
    if is_available is None or not isinstance(is_available, bool):
        return jsonify({"msg": "Valid availability boolean required"}), 400

    donor.availability = is_available
    db.session.commit()
    log_audit_event(user_id, "DONOR_AVAILABILITY_TOGGLED", {"availability": is_available})

    return jsonify({"msg": f"Availability set to {is_available}"}), 200
