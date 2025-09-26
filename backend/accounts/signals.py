from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from .models import StudentProfile, ResearcherProfile, CustomUser
from .utils import export_users_to_json

geolocator = Nominatim(user_agent="myapp")

def geocode_location(city, country):
    try:
        location = geolocator.geocode(f"{city}, {country}")
        if location:
            return location.latitude, location.longitude
    except Exception:
        return None, None
    return None, None


@receiver(post_save, sender=StudentProfile)
def set_student_coordinates(sender, instance, created, **kwargs):
    if (created or not instance.latitude) and instance.city and instance.country:
        lat, lon = geocode_location(instance.city, instance.country)
        if lat and lon:
            instance.latitude = lat
            instance.longitude = lon
            instance.save()


@receiver(post_save, sender=ResearcherProfile)
def set_researcher_coordinates(sender, instance, created, **kwargs):
    if (created or not instance.latitude) and instance.city and instance.country:
        lat, lon = geocode_location(instance.city, instance.country)
        if lat and lon:
            instance.latitude = lat
            instance.longitude = lon
            instance.save()

# Update JSON on create/update
@receiver(post_save, sender=CustomUser)
@receiver(post_save, sender=StudentProfile)
@receiver(post_save, sender=ResearcherProfile)
def update_users_json_on_save(sender, instance, **kwargs):
    export_users_to_json()


# Update JSON on delete
@receiver(post_delete, sender=CustomUser)
@receiver(post_delete, sender=StudentProfile)
@receiver(post_delete, sender=ResearcherProfile)
def update_users_json_on_delete(sender, instance, **kwargs):
    export_users_to_json()

@receiver(post_save, sender=CustomUser)
def update_profile_approval(sender, instance, **kwargs):
    """Sync profile approved field with CustomUser.is_approved."""
    if hasattr(instance, 'studentprofile'):
        if instance.studentprofile.approved != instance.is_approved:
            instance.studentprofile.approved = instance.is_approved
            instance.studentprofile.save()
    if hasattr(instance, 'researcherprofile'):
        if instance.researcherprofile.approved != instance.is_approved:
            instance.researcherprofile.approved = instance.is_approved
            instance.researcherprofile.save()
    # Rebuild JSON
    export_users_to_json()