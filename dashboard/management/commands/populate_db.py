import random

from django.core.management.base import BaseCommand

from customer_addresses.models import CustomerAddress
from customers.factories import CustomerFactory
from customer_addresses.factories import CustomerAddressFactory
from customers.models import Customer
from orders.factories import OrderFactory, OrderItemFactory
from orders.models import OrderItem, Order
from product_reviews.factories import ReviewFactory
from product_reviews.models import Review
from products.factories import (
    ProductFactory,
    BrandFactory,
    CategoryFactory,
    ProductImageFactory,
)
from products.models import Product, ProductImage, Category, Brand


class Command(BaseCommand):
    help = "Populate the database with fake data for all models"

    def handle(self, *args, **options):
        self.stdout.write("Starting database population...")

        # create brand and categories
        brands = self.create_brands(5)
        categories = self.create_categories(5)

        # create products with brands and categories
        products = self.create_products(20, brands, categories)

        # create customers with unique addresses
        self.create_customers(10, 3, 5, 0.4, products)

        self.stdout.write(self.style.SUCCESS("Database population complete."))

    def create_brands(self, number: int) -> list[Brand]:
        return BrandFactory.create_batch(number)

    def create_categories(self, number: int) -> list[Category]:
        return CategoryFactory.create_batch(number)

    def create_product_image(
        self, product: Product, is_main_photo: bool
    ) -> ProductImage:
        return ProductImageFactory.create(product=product, is_main_photo=is_main_photo)

    def create_product_images(
        self, product: Product, number: int
    ) -> list[ProductImage]:
        images = []

        main_img = self.create_product_image(product, True)
        images.append(main_img)

        for _ in range(number - 1):
            non_main_img = self.create_product_image(product, False)
            images.append(non_main_img)

        return images

    def create_products(
        self, number: int, brands: list[Brand], categories: list[Category]
    ) -> list[Product]:
        products = []

        for _ in range(number):
            brand = random.choice(brands)
            category = random.choice(categories)
            product = ProductFactory(brand=brand, category=category)
            self.create_product_images(product, 3)
            products.append(product)

        return products

    def create_address(self) -> CustomerAddress:
        return CustomerAddressFactory()

    def create_order(self, address: CustomerAddress, customer: Customer) -> Order:
        return OrderFactory(address=address, customer=customer)

    def create_order_item(self, order: Order, product: Product) -> OrderItem:
        return OrderItemFactory(order=order, product=product)

    def create_review(self, customer: Customer, product: Product) -> Review:
        return ReviewFactory(author=customer, product=product)

    def create_customers(
        self,
        num_of_customers: int,
        max_num_of_orders: int,
        max_num_of_products: int,
        chance_of_review: float,
        products: list[Product],
    ) -> list[Customer]:
        customers = []

        for _ in range(num_of_customers):
            address = self.create_address()
            customer = CustomerFactory(address=address)

            customers.append(customer)

            for _ in range(random.randint(1, max_num_of_orders)):
                order = self.create_order(address, customer)

                selected_products = random.sample(
                    products, random.randint(1, max_num_of_products)
                )
                for product in selected_products:
                    self.create_order_item(order, product)

                if random.random() < chance_of_review:
                    product_for_review = random.choice(selected_products)
                    self.create_review(customer, product_for_review)

        return customers
