from django.db import models

class Conversation(models.Model):
    user_id = models.CharField(max_length=255, blank=True, null=True)  # For anonymous users, use session ID
    session_id = models.CharField(max_length=255)
    user_message = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    escalated = models.BooleanField(default=False)

    def __str__(self):
        return f"Conversation {self.id} - {self.user_message[:50]}"

class AccountRequest(models.Model):
    user_id = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='pending')  # pending, approved, rejected
    created_at = models.DateTimeField(auto_now_add=True)

class PriceComparison(models.Model):
    product_name = models.CharField(max_length=255)
    nova_price = models.DecimalField(max_digits=10, decimal_places=2)
    competitor_price = models.DecimalField(max_digits=10, decimal_places=2)
    competitor_name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now=True)