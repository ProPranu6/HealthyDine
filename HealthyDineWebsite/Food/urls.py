from django.urls import path
from . import views
from .views import get_homepage
urlpatterns = [  
         path('homepage/', get_homepage),# app homepage
]  