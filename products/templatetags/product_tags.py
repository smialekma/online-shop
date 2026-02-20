from django import template

from django.db.models import Count

register = template.Library()


@register.simple_tag
def get_category_product_count(category_id: int) -> int:
    from products.models import Category

    try:
        category = Category.objects.annotate(products_count=Count("products")).get(
            id=category_id
        )

        return category.products_count
    except Category.DoesNotExist:
        return 0


@register.simple_tag
def get_brand_product_count(brand_id: int) -> int:
    from products.models import Brand

    try:
        brand = Brand.objects.annotate(products_count=Count("products")).get(
            id=brand_id
        )

        return brand.products_count
    except Brand.DoesNotExist:
        return 0


def get_review_count_with_specific_rating(product_id: int, rating: int) -> int:
    from product_reviews.models import Review

    return Review.objects.filter(product_id=product_id, rating=rating).count()


@register.simple_tag
def get_review_count_1(product_id: int) -> int:
    return get_review_count_with_specific_rating(product_id, 1)


@register.simple_tag
def get_review_count_2(product_id: int) -> int:
    return get_review_count_with_specific_rating(product_id, 2)


@register.simple_tag
def get_review_count_3(product_id: int) -> int:
    return get_review_count_with_specific_rating(product_id, 3)


@register.simple_tag
def get_review_count_4(product_id: int) -> int:
    return get_review_count_with_specific_rating(product_id, 4)


@register.simple_tag
def get_review_count_5(product_id: int) -> int:
    return get_review_count_with_specific_rating(product_id, 5)


def get_review_percentage_with_specific_rating(product_id: int, rating: int) -> str:
    from product_reviews.models import Review

    all_reviews: int = Review.objects.filter(product_id=product_id).count()
    reviews_with_rating = get_review_count_with_specific_rating(product_id, rating)

    if all_reviews > 0:
        return f"width: {round((reviews_with_rating/all_reviews) * 100)}%;"
    else:
        return "width: 0%;"


@register.simple_tag
def get_review_percentage_1(product_id: int) -> str:
    return get_review_percentage_with_specific_rating(product_id, 1)


@register.simple_tag
def get_review_percentage_2(product_id: int) -> str:
    return get_review_percentage_with_specific_rating(product_id, 2)


@register.simple_tag
def get_review_percentage_3(product_id: int) -> str:
    return get_review_percentage_with_specific_rating(product_id, 3)


@register.simple_tag
def get_review_percentage_4(product_id: int) -> str:
    return get_review_percentage_with_specific_rating(product_id, 4)


@register.simple_tag
def get_review_percentage_5(product_id: int) -> str:
    return get_review_percentage_with_specific_rating(product_id, 5)
