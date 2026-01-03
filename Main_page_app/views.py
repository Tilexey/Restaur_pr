from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class MainPageView(TemplateView):
    template_name = 'main_page.html'
    context_object_name = 'main_page'