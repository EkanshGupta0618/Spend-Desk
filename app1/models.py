import random
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10)