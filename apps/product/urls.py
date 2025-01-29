from django.urls import path

from apps.product.views.category import CategoryDitailView, CategoryListView
from apps.product.views.product import ProductDetailView, ProductListView

app_name = "product"
urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<slug:slug>/", CategoryDitailView.as_view(), name="category-detail"
    ),
]
