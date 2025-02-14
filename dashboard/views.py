from django.shortcuts import render
from django.views.generic.list import ListView


def home(request):
    return render(request, 'dashboard/home.html')

#class HomeView(ListView):
    # model = Product
    #template_name = "dashboard/base.html"
    # context_object_name = "posts"
    # ordering = ["-date_posted"]
    # paginate_by = 4