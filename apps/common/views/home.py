from django.shortcuts import render

from apps.product.models import Category, Product


def home_view(request):
    products = Product.objects.all()[:10]
    context = {"categories": Category.objects.all(), "products": products}
    return render(request, "index.html", context=context)
