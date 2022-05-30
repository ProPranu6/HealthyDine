from django.urls import path
from . import views

urlpatterns = [  
        path('signup_regular/', views.signup_regular, name="signupreg"),  # app homepage
    path('signup_premium/', views.signup_premium, name='signupprem'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
    
]  