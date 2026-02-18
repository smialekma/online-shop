from django.http import HttpRequest


def checkout_enabled(request: HttpRequest) -> dict[str, bool]:
    cart = request.session.get("cart", {})
    enabled = False
    if cart:
        enabled = True
    return {"checkout_enabled": enabled}
