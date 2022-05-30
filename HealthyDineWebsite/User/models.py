from django.db import models

# Create your models here.
from Food.models import Food

class PremiumUser(models.Model):
    user_id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    mail_id = models.CharField(max_length=30)
    contact_no = models.IntegerField()
    height = models.FloatField()
    weight = models.FloatField()
    calories_intake = models.FloatField(default=2500)
    location = models.CharField(max_length=30)

class RegularUser(models.Model):
    user_id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    mail_id = models.CharField(max_length=30)
    contact_no = models.IntegerField()
    location = models.CharField(max_length=10)

class PreferredFood(models.Model):
    user = models.ForeignKey(PremiumUser, on_delete=models.CASCADE)
    pfood = models.ForeignKey(Food, on_delete = models.CASCADE)
class AllergyFood(models.Model):
    user = models.ForeignKey(PremiumUser, on_delete=models.CASCADE)
    afood = models.CharField(max_length=30)

    