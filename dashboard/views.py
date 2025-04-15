import random

from django.db.models import Count
from django.views.generic import TemplateView
from django.db.models import Prefetch
from products.models import Category, Product, ProductImage

from carts.cart import Cart


# def home(request):
#    return render(request, 'dashboard/home.html',
#                  {
#                      "categories" : Category.objects.all().order_by("name").values(),
#                      "category_display" : Category.objects.all().order_by("name")[:3]
#                  })


def _get_random_products(number_of_products):
    my_ids = Product.objects.values_list("id", flat=True)
    my_ids = list(my_ids)

    rand_ids = random.sample(my_ids, number_of_products)

    random_records = (
        Product.objects.filter(id__in=rand_ids)
        .select_related("category")
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ProductImage.objects.filter(is_main_photo=True),
                to_attr="main_images",
            )
        )
    )

    return random_records


class HomeView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all().order_by("name")
        context["category_display"] = categories[:3]

        context["random_products"] = _get_random_products(6)

        context["top_selling_products"] = []
        context["new_products"] = []

        for category in categories:
            context["new_products"] += (
                Product.objects.all()
                .filter(category=category.id)
                .select_related("category")
                .order_by("date_added")
                .prefetch_related(
                    Prefetch(
                        "images",
                        queryset=ProductImage.objects.filter(is_main_photo=True),
                        to_attr="main_images",
                    )
                )
            )[:5]

            context["top_selling_products"] += (
                Product.objects.all()
                .filter(category=category.id)
                .select_related("category")
                .annotate(count=Count("orders"))
                .order_by("count")
                .prefetch_related(
                    Prefetch(
                        "images",
                        queryset=ProductImage.objects.filter(is_main_photo=True),
                        to_attr="main_images",
                    )
                )
            )[:5]

        context["cart"] = Cart(self.request)
        return context
