from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
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
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="width: 50px; height: 50px; border-radius: 5px;" />'
            )
        return "No image"

    image_preview.short_description = "Image Preview"

    fieldsets = (
        (
            None,
            {"fields": ("name", "category", "description", "image", "image_preview")},
        ),
        (_("Boycott Information"), {"fields": ("is_boycotted", "boycott_reason")}),
        (
            _("Additional Info"),
            {"fields": ("is_kyrgyz_product", "alternative_products")},
        ),
        (_("Statistics"), {"fields": ("query_count",)}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = (
        "query_count",
        "created_at",
        "updated_at",
        "image_preview",
    )  # Добавляем image_preview сюда
    list_display = (
        "name",
        "category",
        "is_boycotted",
        "query_count",
        "get_rating",
        "is_kyrgyz_product",
        "image_preview",
    )
    list_filter = ("category", "is_boycotted", "is_kyrgyz_product")
    search_fields = ("name", "category__name")
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
    search_fields = ("product__name", "user__email")
    ordering = ("-created_at",)
