import factory

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
    "Smartfony",
    "Tablety",
    "Laptopy",
    "Smartwatche i opaski fitness",
    "Słuchawki i zestawy audio",
    "Komputery stacjonarne",
    "Monitory",
    "Klawiatury i myszy",
    "Peryferia i akcesoria",
    "Drukarki i skanery",
    "Konsole do gier",
    "Gry i akcesoria",
    "Fotele gamingowe",
    "Komputery gamingowe",
    "Akcesoria VR",
    "Telewizory",
    "Soundbary i kina domowe",
    "Odtwarzacze multimedialne",
    "Małe AGD",
    "Inteligentny dom",
    "Powerbanki",
    "Ładowarki i adaptery",
    "Baterie i akumulatory",
    "Przedłużacze i listwy zasilające",
    "Panele solarne i stacje ładowania",
    "Podzespoły komputerowe",
    "Obudowy i chłodzenie",
    "Narzędzia serwisowe",
    "Kable i przewody",
    "Uchwyty i stojaki",
]


class BrandFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Brand

    name = factory.Iterator(BRAND_NAMES)


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    name = factory.Iterator(CATEGORY_NAMES)
    photo = factory.django.ImageField()


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"product{n}")
    brand = factory.SubFactory(BrandFactory)
    description = factory.Faker("text", max_nb_chars=200)
    details = factory.Faker("text", max_nb_chars=200)
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    quantity = factory.Faker("random_int", min=0, max=1000000)
    category = factory.SubFactory(CategoryFactory)
    date_added = factory.Faker("date_time")

    is_sale = False
    old_price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)


class ProductImageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductImage

    photo = factory.django.ImageField()
    is_main_photo = factory.Faker("pybool")
    product = factory.SubFactory(ProductFactory)
