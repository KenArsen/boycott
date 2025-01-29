from django.shortcuts import render

from apps.product.models import Category


def home_view(request):
    context = {"categories": Category.objects.all()}
    return render(request, "home.html", context=context)
