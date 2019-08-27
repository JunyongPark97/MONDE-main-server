from django.db import models

# Create your models here.
class Bag(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=20)

