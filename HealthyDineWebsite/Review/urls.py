from django.urls import path
from .views import extract_ratings

urlpatterns = [  
         path('extract_ratings/', extract_ratings, name="rating-extraction")# app homepage
]  