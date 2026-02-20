from django.http import HttpRequest


def rating_options(request: HttpRequest) -> dict[str, tuple[int, ...]]:
    return {"rating_options": (1, 2, 3, 4, 5)}
