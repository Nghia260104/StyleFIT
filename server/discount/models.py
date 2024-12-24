from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import Account

# Create your models here.
class Discount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    percentage = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    price = models.IntegerField()
    season = models.CharField(max_length=50)
    product = models.JSONField() # array of product ids
    # Không thấy có array field và search mạng thấy bảo dùng JSON
    category = models.JSONField() # array of categories
    limit = models.IntegerField()   
    used_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name