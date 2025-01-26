from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import CoreModel
from apps.user.models import User


class Category(CoreModel):
    """Категория товаров (например, Напитки, Косметика)"""

    name = models.CharField(
        max_length=255, unique=True, verbose_name=_("Category name")
    )
    slug = models.SlugField(unique=True, verbose_name=_("Category slug"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Reason(models.Model):
    """Причина бойкота (например, Эксплуатация детского труда, Экологический вред)"""

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Boycott reason")
        verbose_name_plural = _("Boycott reasons")

    def __str__(self):
        return self.title


class Product(CoreModel):
    """Основная модель товара"""

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Category"),
    )
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    is_boycotted = models.BooleanField(default=False, verbose_name=_("Is boycotted"))
    boycott_reason = models.ForeignKey(
        to=Reason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Boycott reason"),
    )
    query_count = models.IntegerField(default=0, verbose_name=_("Query count"))
    is_kyrgyz_product = models.BooleanField(
        default=False, verbose_name=_("Is kyrgyz product")
    )
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name=_("Image")
    )
    alternative_products = models.ManyToManyField(
        to="self", blank=True, verbose_name=_("Alternative products")
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_rating(self):
        """
        Рассчитывает рейтинг от 1 до 5 на основе query_count и отзывов.
        """
        max_queries = (
            Product.objects.filter(category=self.category).aggregate(
                max_queries=models.Max("query_count")
            )["max_queries"]
            or 1
        )
        normalized_query_count = (
            self.query_count / max_queries
        ) * 4  # Нормализуем на основе максимума

        # Рассчитываем средний рейтинг от отзывов
        average_review_rating = (
            self.reviews.aggregate(average_rating=models.Avg("rating"))[
                "average_rating"
            ]
            or 3
        )
        weighted_rating = (
            normalized_query_count + average_review_rating
        ) / 2  # Усредняем запросы и отзывы

        return round(
            min(5, max(1, weighted_rating)), 2
        )  # Ограничиваем рейтинг от 1 до 5

    @classmethod
    def get_sorted_products(cls):
        """
        Получить все продукты, отсортированные по рейтингу.
        """
        products = cls.objects.all()
        sorted_products = sorted(
            products, key=lambda product: product.get_rating(), reverse=True
        )
        return sorted_products


class Review(models.Model):
    """Модель для представления отзыва о товаре"""

    product = models.ForeignKey(
        to=Product,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="reviews",
        verbose_name=_("User"),
    )
    rating = models.IntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        verbose_name=_("Rating"),
    )
    comment = models.TextField(blank=True, verbose_name=_("Comment"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return f"Review for {self.product.name} - Rating: {self.rating}"
