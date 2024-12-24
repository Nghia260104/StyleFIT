from django.db import models
from django.core.exceptions import ValidationError

def validate_base64(value):
    if value and not value.startswith(('data:image/', 'data:application/')):
        raise ValidationError('Invalid base64 format')

# Create your models here.
class Account(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_name = models.CharField(max_length=255)
    authentication_code = models.IntegerField(null=True, blank=True) 
    code_expired = models.DateTimeField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=[
        ('CUSTOMER', 'Customer'),
        ('SELLER', 'Seller'),
        ('ADMIN', 'Admin'),
    ])
    profile_photo = models.TextField(
        null=True,
        blank=True,
        validators=[validate_base64],
        help_text="Base64 encoded image"
    )
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.email