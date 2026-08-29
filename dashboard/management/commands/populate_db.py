# mypy: ignore-errors
from __future__ import annotations

import random
from datetime import timedelta
from decimal import Decimal
from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from customer_addresses.factories import CustomerAddressFactory
from customer_addresses.models import CustomerAddress
from customers.factories import CustomerFactory
from customers.models import Customer
from newsletter.factories import NewsletterPostFactory, SubscriberFactory
from orders.factories import OrderFactory, OrderItemFactory, ShippingMethodFactory
from orders.models import Order, OrderItem, ShippingMethod
from payments.factories import PaymentFactory
from product_reviews.factories import ReviewFactory
from product_reviews.models import Review
from products.factories import (
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductImageFactory,
)
from products.models import Brand, Category, Product, ProductImage
from wishlist.factories import WishlistItemFactory


class Command(BaseCommand):
    help = "Populate the database with coherent fake data for development"

    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Starting database population...")

        brands = self.create_brands(8)
        categories = self.create_categories(5)

        products = [
            *self.create_products(
                20,
                brands,
                categories,
                is_sale=False,
            ),
            *self.create_products(
                10,
                brands,
                categories,
                is_sale=True,
            ),
        ]

        shipping_methods = self.create_shipping_methods()

        customers = self.create_customers(
            num_of_customers=12,
            max_num_of_orders=4,
            max_num_of_products=5,
            chance_of_review=0.75,
            products=products,
            shipping_methods=shipping_methods,
        )

        self.create_wishlist_items(customers, products)
        self.create_newsletter_data()

        self.stdout.write(self.style.SUCCESS("Database population complete."))

    def create_brands(self, number: int) -> list[Brand]:
        return list(BrandFactory.create_batch(number))

    def create_categories(self, number: int) -> list[Category]:
        return list(CategoryFactory.create_batch(number))

    def create_product_image(
        self,
        product: Product,
        is_main_photo: bool,
    ) -> ProductImage:
        return ProductImageFactory.create(
            product=product,
            is_main_photo=is_main_photo,
        )

    def create_product_images(
        self,
        product: Product,
        number: int,
    ) -> list[ProductImage]:
        if number < 1:
            return []

        images = [
            self.create_product_image(
                product,
                True,
            )
        ]

        images.extend(
            self.create_product_image(
                product,
                False,
            )
            for _ in range(number - 1)
        )

        return images

    def create_products(
        self,
        number: int,
        brands: list[Brand],
        categories: list[Category],
        is_sale: bool = False,
    ) -> list[Product]:
        products: list[Product] = []

        for _ in range(number):
            price = Decimal(random.randint(2_000, 400_000)) / Decimal("100")

            if is_sale:
                discount_percent = Decimal(random.randint(10, 40)) / Decimal("100")

                old_price = (price / (Decimal("1") - discount_percent)).quantize(
                    Decimal("0.01")
                )
            else:
                old_price = None

            product = ProductFactory.create(
                brand=random.choice(brands),
                category=random.choice(categories),
                is_sale=is_sale,
                price=price,
                old_price=old_price,
                quantity=random.randint(0, 250),
            )

            self.create_product_images(
                product,
                3,
            )

            products.append(product)

        return products

    def create_shipping_methods(
        self,
    ) -> list[ShippingMethod]:
        return [
            ShippingMethodFactory.create(
                name="Parcel locker",
                price=Decimal("12.99"),
                min_delivery_time_in_days=1,
                max_delivery_time_in_days=2,
            ),
            ShippingMethodFactory.create(
                name="Courier",
                price=Decimal("18.99"),
                min_delivery_time_in_days=1,
                max_delivery_time_in_days=3,
            ),
            ShippingMethodFactory.create(
                name="Economy delivery",
                price=Decimal("7.99"),
                min_delivery_time_in_days=3,
                max_delivery_time_in_days=5,
            ),
        ]

    def create_address(
        self,
        customer: Customer,
    ) -> CustomerAddress:
        return CustomerAddressFactory.create(
            customer=customer,
        )

    def create_order(
        self,
        address: CustomerAddress,
        customer: Customer,
        shipping_method: ShippingMethod,
    ) -> Order:
        created_at = timezone.now() - timedelta(days=random.randint(1, 90))

        date_ordered = created_at + timedelta(minutes=random.randint(1, 120))

        return OrderFactory.create(
            address=address,
            customer=customer,
            email=customer.email,
            shipping_method=shipping_method,
            created_at=created_at,
            date_ordered=date_ordered,
            updated_at=date_ordered,
            date_fulfilled=None,
            total_amount=Decimal("0.00"),
        )

    def create_order_item(
        self,
        order: Order,
        product: Product,
    ) -> OrderItem:
        return OrderItemFactory.create(
            order=order,
            product=product,
            quantity=random.randint(1, 3),
        )

    def update_order_total(
        self,
        order: Order,
    ) -> None:
        items_total = sum(
            (
                item.get_subtotal()
                for item in order.order_items.select_related("product")
            ),
            start=Decimal("0.00"),
        )

        shipping_price = (
            order.shipping_method.price
            if order.shipping_method is not None
            else Decimal("0.00")
        )

        order.total_amount = items_total + shipping_price

        order.save(update_fields=["total_amount"])

    def create_payment(
        self,
        order: Order,
    ) -> None:
        is_paid = random.random() < 0.8

        payment_created_at = order.date_ordered + timedelta(
            minutes=random.randint(1, 30)
        )

        PaymentFactory.create(
            order=order,
            amount=order.total_amount,
            is_paid=is_paid,
            created_at=payment_created_at,
        )

        if is_paid and random.random() < 0.65:
            order.date_fulfilled = payment_created_at + timedelta(
                days=random.randint(1, 5)
            )

            order.updated_at = order.date_fulfilled

            order.save(
                update_fields=[
                    "date_fulfilled",
                    "updated_at",
                ]
            )

    def create_review(
        self,
        customer: Customer,
        product: Product,
    ) -> Review:
        return ReviewFactory.create(
            author=customer,
            product=product,
        )

    def create_customers(
        self,
        num_of_customers: int,
        max_num_of_orders: int,
        max_num_of_products: int,
        chance_of_review: float,
        products: list[Product],
        shipping_methods: list[ShippingMethod] | None = None,
    ) -> list[Customer]:
        customers: list[Customer] = []

        shipping_methods = shipping_methods or self.create_shipping_methods()

        for _ in range(num_of_customers):
            customer = CustomerFactory.create()

            address = self.create_address(customer)

            customers.append(customer)

            reviewed_product_ids: set[int] = set()

            for _ in range(
                random.randint(
                    1,
                    max_num_of_orders,
                )
            ):
                order = self.create_order(
                    address,
                    customer,
                    random.choice(shipping_methods),
                )

                number_of_products = min(
                    random.randint(
                        1,
                        max_num_of_products,
                    ),
                    len(products),
                )

                selected_products = random.sample(
                    products,
                    number_of_products,
                )

                for product in selected_products:
                    self.create_order_item(
                        order,
                        product,
                    )

                self.update_order_total(order)
                self.create_payment(order)

                if random.random() < chance_of_review:
                    review_candidates = [
                        product
                        for product in selected_products
                        if product.pk not in reviewed_product_ids
                    ]

                    if review_candidates:
                        product_for_review = random.choice(review_candidates)

                        self.create_review(
                            customer,
                            product_for_review,
                        )

                        reviewed_product_ids.add(product_for_review.pk)

        return customers

    def create_wishlist_items(
        self,
        customers: list[Customer],
        products: list[Product],
    ) -> None:
        for customer in customers:
            number_of_items = min(
                random.randint(0, 4),
                len(products),
            )

            for product in random.sample(
                products,
                number_of_items,
            ):
                WishlistItemFactory.create(
                    customer=customer,
                    product=product,
                )

    def create_newsletter_data(self) -> None:
        SubscriberFactory.create_batch(10)
        NewsletterPostFactory.create_batch(4)
