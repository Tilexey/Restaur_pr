from django.shortcuts import render
from .models import Dish
from django.db.models import Q
from django.views.generic import ListView

# Create your views here.
class DishView(ListView):
    model = Dish
    template_name = 'dish_list.html'
    context_object_name = 'dishes'
    
    def get_queryset(self):
        #Все страви
        queryset = super().get_queryset()
        
        
        search_query = self.request.GET.get('q')
        
        if search_query:    
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(ingredients__icontains=search_query))
            
        return queryset