from django.contrib import admin

from product_reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "rating", "created_at")

    def has_add_permission(self, request):
        return False
