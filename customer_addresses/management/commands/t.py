from django.core.management.base import BaseCommand
from django.db.models import Prefetch
from operator import attrgetter
from itertools import groupby
from products.models import Category, Product, ProductImage


class Command(BaseCommand):
    def handle(self, *args, **options):
        context = {}
        categories = Category.objects.all().order_by("name")
        # context["category_display"] = categories[:3]
        category_ids = list(categories.values_list("id", flat=True))

        new_products = (
            Product.objects.all()
            .filter(category_id__in=category_ids)
            .order_by("date_added")
            .select_related("category")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_main_photo=True),
                    to_attr="main_images",
                )
            )
        )

        new_products_by_category = {}

        all_new_products = sorted(new_products, key=attrgetter("category_id"))
        for category_id, products in groupby(
            all_new_products, key=attrgetter("category_id")
        ):
            new_products_by_category[category_id] = list(products)[:5]

        print(new_products_by_category)

        print(context)
