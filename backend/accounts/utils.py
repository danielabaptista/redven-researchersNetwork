import os, json
from django.conf import settings
from .models import StudentProfile, ResearcherProfile

def export_users_to_json():
    users_data = []

    # Students
    for student in StudentProfile.objects.all():
        users_data.append({
            "name": student.full_name,
            "city": f"{student.city}, {student.country}",
            "email": student.user.email,
            "university": student.university,
            "uni_acronym": student.university,  # can customize
            "role": "Estudiante",
            "lat": student.latitude,
            "lon": student.longitude,
            "approved": student.approved
        })

    # Researchers
    for researcher in ResearcherProfile.objects.all():
        users_data.append({
            "name": researcher.full_name,
            "city": f"{researcher.city}, {researcher.country}",
            "email": researcher.user.email,
            "university": researcher.alma_mater,
            "uni_acronym": researcher.alma_mater,
            "role": dict(ResearcherProfile.ROLE_CHOICES).get(researcher.role, researcher.role),
            "lat": researcher.latitude,
            "lon": researcher.longitude,
            "approved": researcher.approved
        })

    # Save to static/data/users.json
    output_path = os.path.join(settings.BASE_DIR, "static", "data", "users.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)

    print(f"JSON exported: {len(users_data)} users")  # debug info
    return users_data
