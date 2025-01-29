from django.views.generic import DetailView, ListView

from apps.product.mixins import CategoryMixin
from apps.product.models import Product


class ProductListView(CategoryMixin, ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        return Product.get_sorted_products()


class ProductDetailView(CategoryMixin, DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alternative_products"] = self.object.alternative_products.all()
        return context
