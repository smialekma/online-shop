def checkout_enabled(request):
    cart = request.session.get("cart", {})
    enabled = False
    if cart:
        enabled = True
    return {"checkout_enabled": enabled}
