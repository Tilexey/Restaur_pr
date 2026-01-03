from django.shortcuts import render
from .models import Dish
from django.views.generic import ListView

# Create your views here.
class DishView(ListView):
    model = Dish
    template_name = 'dish_list.html'
    context_object_name = 'dishes'