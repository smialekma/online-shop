from datetime import timezone
from decimal import Decimal

import factory.fuzzy
from factory import LazyAttribute

from .models import Brand, Category, Product, ProductImage

BRAND_NAMES = [
    "Apple",
    "Samsung",
    "Nike",
    "Adidas",
    "Sony",
    "LG",
    "Dell",
    "HP",
    "Lenovo",
    "Asus",
    "Microsoft",
    "Google",
    "Canon",
    "Nikon",
    "Panasonic",
    "Philips",
    "Bosch",
    "Siemens",
    "Xiaomi",
    "Huawei",
]

CATEGORY_NAMES = [
    "Smartphones",
    "Tablets",
    "Laptops",
    "Smartwatches and smart bands",
    "Headphones and ear sets",
    "PCs",
    "Monitors",
    "Keyboards and mice",
    "Accessories",
    "Printers and scanners",
    "Consoles",
    "Games",
    "Gaming chairs",
    "Gaming computers",
    "VR",
    "TVs",
    "Soundbars",
    "Multimedia players",
    "Small appliances",
    "Smart home",
    "Powerbanks",
    "Chargers and adapters",
    "Batteries",
    "Extension cords and power strips",
    "Solar panels and charging stations",
    "Computer components",
    "Cases and cooling",
    "Service tools",
    "Cables and wires",
    "Mounts and stands",
]


class BrandFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Brand

    name = factory.Iterator(BRAND_NAMES)


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Iterator(CATEGORY_NAMES)
    photo = factory.django.ImageField(
        color=factory.fuzzy.FuzzyChoice(
            ["blue", "yellow", "green", "orange", "red", "purple"]
        ),
        height=1,
        width=1,
    )


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"product{n}")
    brand = factory.SubFactory(BrandFactory)
    description = factory.Faker("text", max_nb_chars=200)
    details = factory.Faker("text", max_nb_chars=200)
    old_price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    price = LazyAttribute(lambda obj: obj.old_price + Decimal("5.00"))
    quantity = factory.Faker("random_int", min=0, max=1000000)
    category = factory.SubFactory(CategoryFactory)
    date_added = factory.Faker("date_time", tzinfo=timezone.utc)

    is_sale = False


class ProductImageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductImage

    photo = factory.django.ImageField(
        color=factory.fuzzy.FuzzyChoice(
            ["blue", "yellow", "green", "orange", "red", "purple"]
        ),
        height=1,
        width=1,
    )
    is_main_photo = False
    product = factory.SubFactory(ProductFactory)
