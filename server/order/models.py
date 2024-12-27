from django.db import models
from account.models import Account

# Create your models here.
class Order(models.Model):
    buyer = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    total_price = models.IntegerField() # todo: not sure about this, please change if needed
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled')
    ])

# Pending: When the order is placed but not yet processed.
# Processing: When the order is being prepared for shipment (e.g., packaging).
# Shipped: When the order has been handed over to the shipping carrier.
# Delivered: When the customer has received the order.
# Cancelled: When the order is cancelled before it is shipped.

    def __str__(self):
        return f"Order {self.id} by {self.buyer.email}"
    
