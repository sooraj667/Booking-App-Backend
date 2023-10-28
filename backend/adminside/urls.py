from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path("login/",Login.as_view(),name="Login"),
    path("blockbeaut/",Blockbeaut.as_view(),name="Blockbeaut"),
    path("blockcust/",Blockcust.as_view(),name="Blockcust"),
    path("addnewservice/",Addnewservice.as_view(),name="Addnewservice"),
    
]