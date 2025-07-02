import random

from django.db.models import Count, F
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

    available_products = len(my_ids)
    products_to_get = min(number_of_products, available_products)

    if products_to_get == 0:
        return Product.objects.none()

    rand_ids = random.sample(my_ids, products_to_get)

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

        context["discounted_products"] = (
            Product.objects.all()
            .filter(is_sale=True)
            .select_related("category")
            .annotate(discount=F("old_price") - F("price"))
            .order_by("-discount")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_main_photo=True),
                    to_attr="main_images",
                )
            )
        )[:6]

        context["top_rated_products"] = (
            Product.objects.all()
            .select_related("category")
            .prefetch_related("reviews")
            .order_by("reviews__rating")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_main_photo=True),
                    to_attr="main_images",
                )
            )
        )[:6]

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
                .order_by("-count")
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
