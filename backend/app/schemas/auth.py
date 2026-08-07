import os
from marshmallow import Schema, fields, validate

class RegisterDonorSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    blood_group = fields.Str(required=True, validate=validate.OneOf(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']))
    district = fields.Str(required=True)
    state = fields.Str(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=18, max=65))
    gender = fields.Str(required=True, validate=validate.OneOf(['Male', 'Female', 'Other']))
    weight = fields.Float(required=True, validate=validate.Range(min=45.0))
    # Cloudinary image upload handled by frontend, URL sent here
    profile_image_url = fields.URL(required=False, allow_none=True)

class RegisterHospitalSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100)) # Used for User.name
    hospital_name = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    address = fields.Str(required=True)
    district = fields.Str(required=True)
    state = fields.Str(required=True)
    contact = fields.Str(required=True, validate=validate.Length(min=10, max=20))

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    
class VerifyOTPSchema(Schema):
    email = fields.Email(required=True)
    otp_code = fields.Str(required=True, validate=validate.Length(equal=6))
