from marshmallow import Schema, fields, validate

class UpdateDonorSchema(Schema):
    district = fields.Str(required=False)
    state = fields.Str(required=False)
    age = fields.Int(required=False, validate=validate.Range(min=18, max=65))
    weight = fields.Float(required=False, validate=validate.Range(min=45.0))
    availability = fields.Bool(required=False)
    last_donation = fields.Date(required=False, allow_none=True)
    profile_image_url = fields.URL(required=False, allow_none=True)

class UpdateHospitalSchema(Schema):
    contact = fields.Str(required=False, validate=validate.Length(min=10, max=20))
    address = fields.Str(required=False)

class EmergencyRequestSchema(Schema):
    patient_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    blood_group = fields.Str(required=True, validate=validate.OneOf(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']))
    units_required = fields.Int(required=True, validate=validate.Range(min=1, max=10))
    urgency = fields.Str(required=True, validate=validate.OneOf(['High', 'Medium', 'Low']))
    required_before = fields.DateTime(required=True)
    # Status and flagged_suspicious are set by the backend, not the user

class AdminHospitalVerifySchema(Schema):
    hospital_id = fields.Int(required=True)
    action = fields.Str(required=True, validate=validate.OneOf(['approve', 'reject']))
