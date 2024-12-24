from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import Account
from product.models import Product

# Create your models here.

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    rating = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"Review for {self.product.name} by {self.buyer.email}"