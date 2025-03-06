from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from products.models import Category


#def home(request):
#    return render(request, 'dashboard/home.html',
#                  {
#                      "categories" : Category.objects.all().order_by("name").values(),
#                      "category_display" : Category.objects.all().order_by("name")[:3]
#                  })


class HomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by("name").values()
        context["category_display"] = Category.objects.all().order_by("name")[:3]
        return context
