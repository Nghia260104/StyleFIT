from django.db import models    
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import Account

# Create your models here.
class Discount(models.Model):
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    price = models.IntegerField()
    season = models.CharField(max_length=50)
    # Using ArrayField for PostgreSQL array support
    product = ArrayField(
        models.IntegerField(),
        blank=True,
        help_text="Array of product IDs"
    )
    category = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        help_text="Array of category names"
    )
    limit = models.IntegerField()   
    used_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name