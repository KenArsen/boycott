from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.product.models import Category, Product, Reason, Review


# Админка для Category
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    ordering = ("name",)

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


# Админка для Reason
@admin.register(Reason)
class ReasonAdmin(TranslationAdmin):
    list_display = ("title", "description")
    search_fields = ("title",)
    ordering = ("title",)

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


# Админка для Product
@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = (
        "name",
        "category",
        "is_boycotted",
        "query_count",
        "get_rating",
        "is_kyrgyz_product",
    )
    list_filter = ("category", "is_boycotted", "is_kyrgyz_product")
    search_fields = ("name", "description", "category__name")
    ordering = ("-query_count",)

    class Media:
        js = (
            "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }

    def get_rating(self, obj):
        return obj.get_rating()

    get_rating.short_description = "Rating"


# Админка для Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at", "product")
    search_fields = ("product__name", "user__email", "comment")
    ordering = ("-created_at",)
