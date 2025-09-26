from django.db.models.signals import post_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from .models import StudentProfile, ResearcherProfile

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
