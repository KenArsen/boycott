from apps.product.models import Category


class CategoryMixin:
    """Миксин для добавления списка категорий в контекст шаблона"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
