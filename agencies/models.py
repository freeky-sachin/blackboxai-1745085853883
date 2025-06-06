from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('agency_user', 'Agency User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    role = models.CharField(max_length=20, choices=USER_ROLES, default='agency_user')

    def __str__(self):
        return f"{self.user.username} Profile"
        
class Agency(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

class EmergencyAlert(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Location(models.Model):
    agency = models.OneToOneField(Agency, on_delete=models.CASCADE, related_name='location')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Location of {self.agency.name}"
