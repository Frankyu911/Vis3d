"""Vis3d URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from Visdate import views

urlpatterns = [
    path('', views.index, name='index'),
    path('easyMode/', views.easyMode, name='easyMode'),
    path('accurateMode/', views.accurateMode, name='accurateMode'),
    path('compareMode/', views.compareMode, name='compareMode'),
    path('calculateMode/', views.calculateMode, name='calculateMode'),
    path('accurateUpload/',views.accurateUpload,),
    path('easyUpload/',views.easyUpload,),
    path('calculateUpload/',views.calculateUpload,),
    path('compareUpload/',views.compareUpload,),
    path('save/',views.save,),
    path('update/',views.update,),
    path('about/',views.about,name='about')
]
