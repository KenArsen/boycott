from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import TemplateView

from apps.product.models import Category, Product


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get("search", "")

        # Базовый QuerySet
        queryset = Product.objects.all()

        # Применяем фильтры поиска, если они указаны
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Настройка пагинации
        paginator = Paginator(queryset, 10)  # 10 элементов на страницу
        page = self.request.GET.get("page")

        try:
            paginated_objects = paginator.page(page)
        except PageNotAnInteger:
            # Если page не целое число, отображаем первую страницу
            paginated_objects = paginator.page(1)
        except EmptyPage:
            # Если page больше чем количество страниц, отображаем последнюю
            paginated_objects = paginator.page(paginator.num_pages)

        # Добавляем пагинированные объекты в контекст
        context["boycotted_products"] = paginated_objects
        context["categories"] = Category.objects.all()

        # Сохраняем параметры поиска для сохранения их при пагинации
        context["search_query"] = search_query

        return context
