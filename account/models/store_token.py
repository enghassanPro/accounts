from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class Store_Token(models.Model):
    token = models.CharField(max_length=250 , unique=True , editable=False)
    created = models.DateTimeField(default=now)
