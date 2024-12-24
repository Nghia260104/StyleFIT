from django.db import models
from account.models import Account
from review.models import Review

# Create your models here.
class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"Reply to review {self.review.product.name} by {self.account.email}"  