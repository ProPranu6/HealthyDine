from django.contrib import admin
from .models import PremiumUser, RegularUser, PreferredFood, AllergyFood

# Register your models here.
admin.site.register(PremiumUser)
admin.site.register(RegularUser)
admin.site.register(PreferredFood)
admin.site.register(AllergyFood)