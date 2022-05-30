from django.db import models

from Food.models import Food
from User.models import PremiumUser, PreferredFood

# Create your models here.

class Order(models.Model):
    usr_id = models.IntegerField()
    food_id = models.IntegerField()
    quant = models.IntegerField()
    
    def extract_food_interests(self, usr_id):
        
        if usr_id == self.usr_id:
            usr_obj = PremiumUser.objects.raw("select * from user_premiumuser where id = %s", [self.usr_id])[0]
            
            food_obj = Food.objects.raw("select * from food_food where id = %s", [self.food_id])[0]
            
            return [(usr_obj, food_obj)]
        
        return []
            
            
    

    