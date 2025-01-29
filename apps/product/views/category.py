from django.views.generic import DetailView, ListView

from apps.product.models import Category


class CategoryListView(ListView):
    model = Category
    template_name = "product/category_list.html"
    context_object_name = "categories"
    paginate_by = 10


class CategoryDitailView(DetailView):
    model = Category
    template_name = "product/category_detail.html"
    context_object_name = "category"
