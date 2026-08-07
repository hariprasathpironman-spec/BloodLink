from datetime import datetime, timezone, date

COMPATIBILITY_MAP = {
    'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
    'O+': ['O+', 'A+', 'B+', 'AB+'],
    'A-': ['A-', 'A+', 'AB-', 'AB+'],
    'A+': ['A+', 'AB+'],
    'B-': ['B-', 'B+', 'AB-', 'AB+'],
    'B+': ['B+', 'AB+'],
    'AB-': ['AB-', 'AB+'],
    'AB+': ['AB+']
}

def compatible_blood_group(donor_bg: str, request_bg: str) -> bool:
    """Check if the donor's blood group is compatible with the request's blood group."""
    if donor_bg not in COMPATIBILITY_MAP:
        return False
    return request_bg in COMPATIBILITY_MAP[donor_bg]

def get_match_badge(score: int) -> str:
    """Returns the matching tier badge label based on the deterministic score."""
    if score >= 85:
        return "Best Match"
    elif score >= 65:
        return "Good Match"
    else:
        return "Average Match"

def calculate_match_score(donor, request) -> dict:
    """
    Calculates the deterministic AI match score based on the user-defined formula.
    Returns a dict with the score and the badge label.
    """
    score = 0
    
    # Blood Group Matching
    if donor.blood_group == request.blood_group:
        score += 40
    elif compatible_blood_group(donor.blood_group, request.blood_group):
        score += 25
        
    # Location Matching
    if donor.district == request.district: # Assuming request inherits hospital's district
        score += 20
    elif donor.state == request.state:
        score += 10
        
    # Availability
    if donor.availability:
        score += 15
        
    # Donation Recency
    if donor.last_donation is None:
        # Never donated before or not recorded, we'll treat it as >= 90 days
        score += 15
    else:
        today = date.today()
        # Convert last_donation to date if it's datetime
        last_donation_date = donor.last_donation.date() if isinstance(donor.last_donation, datetime) else donor.last_donation
        days_since_donation = (today - last_donation_date).days
        
        if days_since_donation >= 90:
            score += 15
        elif days_since_donation >= 60:
            score += 8
            
    # Age Constraint
    if 18 <= donor.age <= 55:
        score += 10
        
    score = min(score, 100)
    badge = get_match_badge(score)
    
    return {
        "score": score,
        "badge": badge
    }
