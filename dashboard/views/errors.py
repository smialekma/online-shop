from typing import Any

from django.http import HttpResponse
from django.shortcuts import render


def handler404(request, *args: Any, **argv: Any) -> HttpResponse:
    context = {
        "code": "404",
        "title": "Page not found",
        "description": "The page you’re looking for doesn’t exist or has been moved.",
    }
    response = render(request, "dashboard/error.html", context=context, status=404)
    return response


def handler403(request, *args: Any, **argv: Any) -> HttpResponse:
    context = {
        "code": "403",
        "title": "Access denied",
        "description": "You don’t have permission to access this page.",
    }
    response = render(request, "dashboard/error.html", context=context, status=404)
    return response


def handler500(request, *args: Any, **argv: Any) -> HttpResponse:
    context = {
        "code": "500",
        "title": "Server error",
        "description": "An unexpected error occurred on our side. Please try again later.",
    }
    response = render(request, "dashboard/error.html", context=context, status=404)
    return response
