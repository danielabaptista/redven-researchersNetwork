from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="redven_app")

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password=password, user_type="admin", **extra_fields)
        user.is_approved = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("researcher", "Researcher"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    university = models.CharField(max_length=200)
    bachelor_degree = models.CharField(max_length=100)
    approved = models.BooleanField(default=False) 
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def geocode_location(self):
        if not self.latitude or not self.longitude:
            try:
                location = geolocator.geocode(f"{self.city}, {self.country}")
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                    self.save(update_fields=["latitude","longitude"])
            except GeocoderTimedOut:
                pass

    def __str__(self):
        return self.full_name


class ResearcherProfile(models.Model):
    ROLE_CHOICES = (
        ('professor','Profesor'),
        ('phd','Estudiante de Doctorado'),
        ('master','Estudiante de Maestría'),
        ('postdoc','Investigador Postdoctoral'),
        ('researcher','Investigador'),
        ('other','Otro'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    alma_mater = models.CharField(max_length=200)
    current_university = models.CharField(max_length=200)
    bachelor_degree = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    approved = models.BooleanField(default=False) 
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def geocode_location(self):
        if not self.latitude or not self.longitude:
            try:
                location = geolocator.geocode(f"{self.city}, {self.country}")
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                    self.save(update_fields=["latitude","longitude"])
            except GeocoderTimedOut:
                pass

    def __str__(self):
        return self.full_name
