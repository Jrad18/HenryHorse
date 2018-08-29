from django.db import models
from jsonfield import JSONField

# Create your models here.
class Horses(models.Model):
    name = models.CharField(max_length=255)

class Jockeys(models.Model):
    name = models.CharField(max_length=255)

class Tracks(models.Model):
    name = models.CharField(max_length=255)

class Forms(models.Model):
    date = models.DateTimeField('date')
    form_data = JSONField()