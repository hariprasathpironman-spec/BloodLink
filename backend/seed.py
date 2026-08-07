import os
import sys
from datetime import datetime, timezone, timedelta
import random

# Add app to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.donor import Donor
from app.models.hospital import Hospital
from app.models.admin import Admin
from app.models.request import EmergencyRequest
from app.utils.security import hash_password

TAMIL_NADU_DISTRICTS = [
    "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", 
    "Salem", "Tirunelveli", "Erode", "Vellore", "Thoothukudi"
]

TAMIL_NAMES = [
    "Karthik S.", "Priya M.", "Rajesh K.", "Divya T.", 
    "Arun J.", "Sita R.", "Murugan V.", "Anjali P."
]

def seed_database():
    app = create_app()
    with app.app_context():
        # Create all tables (useful for first-time setup before migrations)
        db.create_all()

        print("Checking for existing Admin...")
        if not User.query.filter_by(email="admin@bloodlink.gov.in").first():
            print("Seeding Admin account...")
            admin_user = User(
                name="System Administrator",
                email="admin@bloodlink.gov.in",
                password_hash=hash_password("SuperSecureAdmin2026!"),
                role="admin",
                verified=True
            )
            db.session.add(admin_user)
            db.session.flush()

            admin_profile = Admin(
                id=admin_user.id,
                totp_secret="JBSWY3DPEHPK3PXP" # Mock static secret for testing
            )
            db.session.add(admin_profile)
        
        print("Checking for existing Donors...")
        if Donor.query.count() < 5:
            print("Seeding Donors...")
            for i in range(5):
                name = random.choice(TAMIL_NAMES)
                donor_user = User(
                    name=name,
                    email=f"donor{i}@example.com",
                    password_hash=hash_password("DonorPassword123"),
                    role="donor",
                    verified=True
                )
                db.session.add(donor_user)
                db.session.flush()

                donor_profile = Donor(
                    donor_id=donor_user.id,
                    blood_group=random.choice(["O+", "A+", "B+", "AB+", "O-", "A-"]),
                    district=random.choice(TAMIL_NADU_DISTRICTS),
                    state="Tamil Nadu",
                    age=random.randint(18, 55),
                    gender=random.choice(["Male", "Female"]),
                    weight=random.uniform(50.0, 85.0),
                    availability=True,
                    last_donation=datetime.now(timezone.utc) - timedelta(days=random.randint(30, 150))
                )
                db.session.add(donor_profile)

        print("Checking for existing Hospitals...")
        if Hospital.query.count() == 0:
            print("Seeding Hospitals...")
            
            # Unverified Hospital
            unverified_hosp_user = User(
                name="Dr. Sekar",
                email="contact@gh-madurai.in",
                password_hash=hash_password("HospitalPass123"),
                role="hospital",
                verified=True # Email verified, but hospital profile is not
            )
            db.session.add(unverified_hosp_user)
            db.session.flush()
            
            unverified_hosp = Hospital(
                hospital_id=unverified_hosp_user.id,
                hospital_name="Government Hospital Madurai",
                address="123 Main Road, Madurai",
                district="Madurai",
                state="Tamil Nadu",
                contact="9876543210",
                verification_doc_url="https://res.cloudinary.com/demo/image/upload/sample.jpg",
                verified=False
            )
            db.session.add(unverified_hosp)

            # Verified Hospital
            verified_hosp_user = User(
                name="Dr. Lakshmi",
                email="admin@apollo-chennai.in",
                password_hash=hash_password("HospitalPass123"),
                role="hospital",
                verified=True 
            )
            db.session.add(verified_hosp_user)
            db.session.flush()
            
            admin_id = User.query.filter_by(role='admin').first().id

            verified_hosp = Hospital(
                hospital_id=verified_hosp_user.id,
                hospital_name="Apollo Main Hospital",
                address="Greams Road, Chennai",
                district="Chennai",
                state="Tamil Nadu",
                contact="9988776655",
                verification_doc_url="https://res.cloudinary.com/demo/image/upload/sample.jpg",
                verified=True,
                verified_by_admin_id=admin_id
            )
            db.session.add(verified_hosp)
            db.session.flush()

            # Seed an Emergency Request for the verified hospital
            print("Seeding Emergency Request...")
            req = EmergencyRequest(
                patient_name="Vijay T.",
                blood_group="O+",
                units_required=2,
                urgency="High",
                required_before=datetime.now(timezone.utc) + timedelta(hours=12),
                hospital_id=verified_hosp.hospital_id,
                status="Open",
                flagged_suspicious=False
            )
            db.session.add(req)

        db.session.commit()
        print("✅ Database Seeded Successfully!")

if __name__ == "__main__":
    seed_database()
