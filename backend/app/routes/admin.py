from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.extensions import db
from app.models.hospital import Hospital
from app.models.user import User
from app.schemas.api import AdminHospitalVerifySchema
from app.utils.security import admin_required
from app.utils.audit import log_audit_event

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/hospitals/pending', methods=['GET'])
@jwt_required()
@admin_required()
def get_pending_hospitals():
    hospitals = Hospital.query.filter_by(verified=False).all()
    res = []
    for h in hospitals:
        res.append({
            "hospital_id": h.hospital_id,
            "hospital_name": h.hospital_name,
            "email": h.user.email,
            "district": h.district,
            "contact": h.contact,
            "verification_doc_url": h.verification_doc_url
        })
    return jsonify(res), 200

@admin_bp.route('/hospitals/verify', methods=['POST'])
@jwt_required()
@admin_required()
def verify_hospital():
    admin_id = get_jwt_identity()
    try:
        data = AdminHospitalVerifySchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
        
    hospital = Hospital.query.get(data['hospital_id'])
    if not hospital:
        return jsonify({"msg": "Hospital not found"}), 404
        
    if data['action'] == 'approve':
        hospital.verified = True
        hospital.verified_by_admin_id = int(admin_id)
        msg = "Hospital approved successfully."
    else:
        # Rejection logic: Delete the unverified user and hospital profile
        user = hospital.user
        db.session.delete(user)
        msg = "Hospital rejected and account deleted."
        
    db.session.commit()
    log_audit_event(int(admin_id), f"HOSPITAL_{data['action'].upper()}", {"hospital_id": data['hospital_id']})
    
    return jsonify({"msg": msg}), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_user(user_id):
    admin_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    if user.role == 'admin':
        return jsonify({"msg": "Cannot delete admin users via this endpoint"}), 403
        
    role = user.role
    email = user.email
    db.session.delete(user)
    db.session.commit()
    
    log_audit_event(admin_id, "USER_DELETED", {"deleted_user_id": user_id, "role": role, "email": email})
    
    return jsonify({"msg": "User account successfully deleted"}), 200
