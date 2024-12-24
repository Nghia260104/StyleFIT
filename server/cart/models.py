from django.db import models
from account.models import Account
from product.models import Product

# Create your models here.
class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.account.email} - {self.product.name}"
