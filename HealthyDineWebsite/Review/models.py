from django.db import models

# Create your models here.

from Food.models import Food
class Review(models.Model):
    rev_type = models.CharField(max_length=20) #discrete, descriptive
    rev_content = models.CharField(max_length=300, default='none')
    rev_rating = models.IntegerField(default=0)
    food_id = models.IntegerField()
    