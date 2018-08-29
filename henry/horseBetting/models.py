from django.db import models
from jsonfield import JSONField
import json

# Create your models here.
class Horses(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Jockeys(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Tracks(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Forms(models.Model):
    date = models.DateTimeField('date')
    form_data = JSONField()
    def datadump(self):
        return json.dumps(self.form_data, sort_keys=True, indent=4)

