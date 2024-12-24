from django.db import models
from account.models import Account

# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity_in_stock = models.IntegerField(default=0)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name