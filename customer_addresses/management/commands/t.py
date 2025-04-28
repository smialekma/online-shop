from django.core.management.base import BaseCommand
from django.db.models import Prefetch, Count
from products.models import Product, ProductImage
from icecream import ic


class Command(BaseCommand):
    def handle(self, *args, **options):
        products = (
            (
                (
                    Product.objects.all()
                    .select_related("category")
                    .annotate(count=Count("orders"))
                ).order_by("-count")
            ).prefetch_related(
                Prefetch(
                    "images",
                    queryset=ProductImage.objects.filter(is_main_photo=True),
                    to_attr="main_images",
                )
            )
        )[:3]

        ic(products)

        # limit = 5
        # product = Product.objects.get(id=1)
        # order_ids = OrderItem.objects.filter(product_id=product).values_list('order_id', flat=True)
        #
        # ic(order_ids)
        #
        # related_products_ids = OrderItem.objects.filter(
        #     order_id__in=order_ids
        # ).exclude(
        #     product_id=product
        # ).values_list('product_id', flat=True)
        #
        # ic(related_products_ids)
        #
        # products_counts = OrderItem.objects.filter(
        #     product_id__in=related_products_ids
        # ).values('product_id').annotate(
        #     count=Count('product_id')
        # ).order_by('-count')
        #
        # ic(products_counts)
        #
        # related_products = []
        #
        # for item in products_counts[:limit]:
        #     product = Product.objects.get(id=item['product_id'])
        #     related_products.append(product)
        #
        # print(related_products)

        # context = {}
        # categories = Category.objects.all().order_by("name")
        # # context["category_display"] = categories[:3]
        # category_ids = list(categories.values_list("id", flat=True))
        #
        # new_products = (
        #     Product.objects.all()
        #     .filter(category_id__in=category_ids)
        #     .order_by("date_added")
        #     .select_related("category")
        #     .prefetch_related(
        #         Prefetch(
        #             "images",
        #             queryset=ProductImage.objects.filter(is_main_photo=True),
        #             to_attr="main_images",
        #         )
        #     )
        # )
        #
        # new_products_by_category = {}
        #
        # all_new_products = sorted(new_products, key=attrgetter("category_id"))
        # for category_id, products in groupby(
        #     all_new_products, key=attrgetter("category_id")
        # ):
        #     new_products_by_category[category_id] = list(products)[:5]
        #
        # print(new_products_by_category)
        #
        # print(context)
