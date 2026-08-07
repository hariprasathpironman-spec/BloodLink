from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from datetime import datetime, timezone

from app.extensions import db, limiter
from app.models.user import User
from app.models.donor import Donor
from app.models.hospital import Hospital
from app.schemas.auth import (
    RegisterDonorSchema, RegisterHospitalSchema,
    LoginSchema, VerifyOTPSchema
)
from app.utils.security import hash_password, verify_password
from app.utils.email import generate_otp, get_otp_expiry, send_otp_email
from app.utils.audit import log_audit_event

auth_bp = Blueprint('auth', __name__)


# ─────────────────────────────────────────────
#  REGISTER DONOR
# ─────────────────────────────────────────────
@auth_bp.route('/register/donor', methods=['POST'])
@limiter.limit("3 per minute")
def register_donor():
    try:
        data = RegisterDonorSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already registered"}), 409

    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hash_password(data['password']),
        role='donor',
        verified=False
    )
    db.session.add(new_user)
    db.session.flush()

    new_donor = Donor(
        donor_id=new_user.id,
        blood_group=data['blood_group'],
        district=data['district'],
        state=data['state'],
        age=data['age'],
        gender=data['gender'],
        weight=data['weight'],
        profile_image_url=data.get('profile_image_url')
    )
    db.session.add(new_donor)

    otp = generate_otp()
    new_user.otp_code = otp
    new_user.otp_expiry = get_otp_expiry()
    db.session.commit()

    # Send OTP — non-fatal (fallback OTP printed to Railway logs if email fails)
    send_otp_email(new_user.email, otp)

    log_audit_event(new_user.id, "DONOR_REGISTERED", {"email": new_user.email})

    return jsonify({
        "msg": "Donor registered successfully. Check your email for the OTP verification code."
    }), 201


# ─────────────────────────────────────────────
#  REGISTER HOSPITAL
# ─────────────────────────────────────────────
@auth_bp.route('/register/hospital', methods=['POST'])
@limiter.limit("3 per minute")
def register_hospital():
    try:
        data = RegisterHospitalSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already registered"}), 409

    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hash_password(data['password']),
        role='hospital',
        verified=False
    )
    db.session.add(new_user)
    db.session.flush()

    new_hospital = Hospital(
        hospital_id=new_user.id,
        hospital_name=data['hospital_name'],
        address=data['address'],
        district=data['district'],
        state=data['state'],
        contact=data['contact'],
        verification_doc_url="",
        verified=False
    )
    db.session.add(new_hospital)

    otp = generate_otp()
    new_user.otp_code = otp
    new_user.otp_expiry = get_otp_expiry()
    db.session.commit()

    # Send OTP — non-fatal
    send_otp_email(new_user.email, otp)

    log_audit_event(new_user.id, "HOSPITAL_REGISTERED",
                    {"hospital_name": new_hospital.hospital_name})

    return jsonify({
        "msg": "Hospital registered successfully. Check your email for the OTP verification code."
    }), 201


# ─────────────────────────────────────────────
#  VERIFY OTP
# ─────────────────────────────────────────────
@auth_bp.route('/verify-otp', methods=['POST'])
@limiter.limit("5 per minute")
def verify_otp():
    try:
        data = VerifyOTPSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.verified:
        return jsonify({"msg": "Email already verified. Please login."}), 400

    if not user.otp_code or not user.otp_expiry:
        return jsonify({"msg": "No OTP found. Please register again."}), 400

    if datetime.now(timezone.utc) > user.otp_expiry.replace(tzinfo=timezone.utc):
        return jsonify({"msg": "OTP has expired. Please click Resend OTP."}), 400

    if user.otp_code != data['otp_code']:
        return jsonify({"msg": "Invalid OTP. Please check and try again."}), 400

    user.verified = True
    user.otp_code = None
    user.otp_expiry = None
    db.session.commit()

    log_audit_event(user.id, "EMAIL_VERIFIED", {"email": user.email})

    return jsonify({"msg": "Email verified successfully! You can now login."}), 200


# ─────────────────────────────────────────────
#  RESEND OTP
# ─────────────────────────────────────────────
@auth_bp.route('/resend-otp', methods=['POST'])
@limiter.limit("1 per minute")
def resend_otp():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"msg": "Email is required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.verified:
        return jsonify({"msg": "Email already verified. Please login."}), 400

    otp = generate_otp()
    user.otp_code = otp
    user.otp_expiry = get_otp_expiry()
    db.session.commit()

    send_otp_email(user.email, otp)

    return jsonify({"msg": "New OTP sent! Check your email inbox."}), 200


# ─────────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────────
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    try:
        data = LoginSchema().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not verify_password(data['password'], user.password_hash):
        return jsonify({"msg": "Invalid email or password"}), 401

    if not user.verified:
        return jsonify({
            "msg": "Please verify your email first. Check your inbox for the OTP."
        }), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(identity=str(user.id))

    log_audit_event(user.id, "USER_LOGIN", {"role": user.role})

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200


# ─────────────────────────────────────────────
#  REFRESH TOKEN
# ─────────────────────────────────────────────
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.get(identity)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    access_token = create_access_token(
        identity=identity,
        additional_claims={"role": user.role}
    )
    return jsonify(access_token=access_token)
