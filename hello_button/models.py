from django.db import models

# Create your models here.
class LabMembers(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
    )
