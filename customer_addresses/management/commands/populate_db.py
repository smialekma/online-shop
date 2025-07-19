import random

from django.core.management.base import BaseCommand

from customers.factories import CustomerFactory
from customer_addresses.factories import CustomerAddressFactory
from orders.factories import OrderFactory, OrderItemFactory
from product_reviews.factories import ReviewFactory
from products.factories import (
    ProductFactory,
    BrandFactory,
    CategoryFactory,
    ProductImageFactory,
)


class Command(BaseCommand):
    help = "Populate the database with fake data for all models"

    def handle(self, *args, **options):
        self.stdout.write("Starting database population...")
        customers = []
        products = []

        # create brand and categories
        brands = BrandFactory.create_batch(5)
        categories = CategoryFactory.create_batch(5)

        # create products with brands and categories
        for _ in range(20):
            brand = random.choice(brands)
            category = random.choice(categories)
            product = ProductFactory(brand=brand, category=category)
            ProductImageFactory.create(product=product, is_main_photo=True)
            ProductImageFactory.create(product=product, is_main_photo=False)
            ProductImageFactory.create(product=product, is_main_photo=False)
            products.append(product)

        # create customers with unique addresses
        for _ in range(10):
            address = CustomerAddressFactory()
            customer = CustomerFactory(address=address)
            customers.append(customer)

            # each customer has 1-3 orders
            for _ in range(random.randint(1, 3)):
                order = OrderFactory(address=address, customer=customer)

                # there is 1-5 products in each order
                selected_products = random.sample(products, random.randint(1, 5))
                for product in selected_products:
                    OrderItemFactory(order=order, product=product)

                # sometimes customer leaves a review of 1 product
                if random.random() < 0.4:  # 40% chance
                    product_for_review = random.choice(selected_products)
                    ReviewFactory(author=customer, product=product_for_review)

        self.stdout.write(self.style.SUCCESS("Database population complete."))
