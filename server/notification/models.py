from django.db import models
from account.models import Account
from reply.models import Reply
from order.models import Order

# Create your models here.
class Notification(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=[
        ('REVIEW', 'New Review'),
        ('ORDER', 'New Order'),
        ('REPLY', 'New Reply'),
        ('STATUS', 'Order Status Update'),
    ])
    content = models.TextField()
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    read = models.BooleanField(default=False)
    partner = models.ForeignKey(Account, on_delete=models.CASCADE, null = True, related_name='partner_notifications')

    def __str__(self):
        return f"Notification for {self.account.email}: {self.type}"