from django.contrib import admin
from .views import DishView
from django.urls import path

urlpatterns = [
    path('', DishView.as_view())
]