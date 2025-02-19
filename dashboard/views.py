from django.shortcuts import render
from django.views.generic.list import ListView
from products.models import Category


def home(request):
    return render(request, 'dashboard/home.html',
                  {"categories" : Category.objects.all(), "category_display" : Category.objects.all()[:3]})

#class HomeView(ListView):
    # model = Product
    #template_name = "dashboard/base.html"
    # context_object_name = "posts"
    # ordering = ["-date_posted"]
    # paginate_by = 4