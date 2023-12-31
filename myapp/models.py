from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Notes(models.Model):
    body = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.body)
