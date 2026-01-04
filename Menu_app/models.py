from django.db import models

# Create your models here.
class Dish(models.Model):
    image = models.ImageField(upload_to='static/', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.CharField(max_length=400, null=True, blank=True)
    

    