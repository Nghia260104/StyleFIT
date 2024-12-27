from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.
class Account(AbstractUser):
    # Attributes
    email = models.EmailField(unique=True)
    password = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    profile_name = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)
    role = models.CharField(choices=[
        ('CUSTOMER', 'Customer'),
        ('SELLER', 'Seller'),
        ('ADMIN', 'Admin'),
    ])
    profile_photo = models.TextField(
        null=True,
        blank=True,
        help_text='Base64 encoded image'
    )
    phone = models.CharField(max_length=15)
    address = models.TextField(null=True)
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['email', 'role'], name='unique_email_role')
    #     ]
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'profile_name']
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def __str__(self):
        return self.email