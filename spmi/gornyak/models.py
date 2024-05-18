from django.db import models

class Events(models.Model):
    title = models.CharField(max_length=255)

# Create your models here.
