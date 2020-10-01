from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now=True)
