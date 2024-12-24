from django.db import models
from order.models import Order
from product.models import Product

# Create your models here.
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name}"
    
