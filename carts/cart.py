from decimal import Decimal
from django.http import HttpRequest
from typing import Iterator, TypedDict
from django.conf import settings

from products.models import Product


class CartItem(TypedDict):
    quantity: int
    price: str
    total_price: float


class Cart:
    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self) -> None:
        self.session.modified = True

    def upsert(
        self, product: Product, quantity: int = 1, override_quantity: bool = False
    ) -> None:
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "total_price": 0,
            }
        item = self.cart[product_id]

        if override_quantity:
            item["quantity"] = quantity
        else:
            item["quantity"] += quantity

        item["total_price"] = float(item["quantity"]) * float(item["price"])

        self.save()

    def remove(self, product_id: int) -> None:
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def get_item(self, product_id: int):
        return self.cart.get(str(product_id))

    def __iter__(self) -> Iterator[CartItem]:
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            main_image = product.images.filter(is_main_photo=True).first()
            cart[str(product.pk)]["product"] = {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
                "main_image_url": main_image.photo.url if main_image else None,
            }

        for item in cart.values():
            item["total_price"] = str(
                float(item["product"]["price"]) * item["quantity"]
            )
            item["price"] = str(item["product"]["price"])
            yield item

    def __len__(self) -> int:
        return sum(item["quantity"] for item in self.cart.values())

    def count_unique_items(self) -> int:
        return len(self.cart)

    def get_sub_total_price(self) -> Decimal:
        return Decimal(
            sum(
                Decimal(item["price"]) * Decimal(item["quantity"])
                for item in self.cart.values()
            )
        )

    def get_total_price(self) -> Decimal:
        return Decimal(
            sum(
                Decimal(item["price"]) * Decimal(item["quantity"])
                for item in self.cart.values()
            )
        )

    def clear(self) -> None:
        """
        Remove all items from the cart.
        """
        for key in list(self.cart.keys()):  # Use list() to create a copy of keys
            del self.cart[key]
        self.save()
