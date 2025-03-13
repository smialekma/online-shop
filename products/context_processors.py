from .models import Category
from carts.cart import Cart


def categories(request):
    return {'categories': Category.objects.all().prefetch_related('products')}


def cart(request):
    return {"cart": Cart(request)}
