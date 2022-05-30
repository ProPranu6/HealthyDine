"""DJhealthydine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from User.views import intro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_food/', include('Food.urls')),
    path('users/', include('User.urls')),
    path('food/', include('Food.urls')),
    path('review/', include('Review.urls')),
    path('', intro, name='intro'), 
    path('orders/', include('Orders.urls')),
    
]

urlpatterns += staticfiles_urlpatterns()