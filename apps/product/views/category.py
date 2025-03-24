from django.views.generic import DetailView, ListView

from apps.product.models import Category


class CategoryListView(ListView):
    model = Category
    template_name = "pages/category.html"
    context_object_name = "categories"
    paginate_by = 10


class CategoryDitailView(DetailView):
    model = Category
    template_name = "pages/category.html"
    context_object_name = "category"
