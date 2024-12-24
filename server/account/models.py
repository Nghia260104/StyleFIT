from django.db import models

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
        ('CUSTOMER', 'Customer')
        ('SELLER', 'Seller')
        ('ADMIN', 'Admin')  
    ])
    profile_photo = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.email