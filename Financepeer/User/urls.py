from django.contrib import admin
from django.urls import path,include
from User.views import *

urlpatterns = [
    path("LogOut",LogOut.as_view()),
]