from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from typing import Optional


class NodeContact(models.Model):
    """
    Модель для хранения контактной информации для звена.
    Связана с моделью GridNode.
    """
    grid_node = models.OneToOneField(
        "GridNode", on_delete=models.CASCADE, related_name="contact_info"
    )
    email: str = models.EmailField(verbose_name="Email")
    country: str = models.CharField(max_length=100, verbose_name="Страна")
    city: str = models.CharField(max_length=100, verbose_name="Город")
    street: str = models.CharField(max_length=100, verbose_name="Улица")
    building: str = models.CharField(max_length=10, verbose_name="Дом")

    class Meta:
        verbose_name = "Контакт звена"
        verbose_name_plural = "Контакты звеньев"

    def __str__(self) -> str:
        """
        Возвращает строковое представление контакта звена.
        """
        return f"{self.country}, {self.city}, {self.street}, {self.building}"


class EliteProduct(models.Model):
    """
    Модель для хранения информации о продукте в сети.
    """
    name: str = models.CharField(max_length=100, verbose_name="Название")
    model: str = models.CharField(max_length=50, verbose_name="Модель")
    release_date: models.DateField = models.DateField(verbose_name="Дата выхода")

    class Meta:
        verbose_name = "Продукт EliteGrid"
        verbose_name_plural = "Продукты EliteGrid"

    def __str__(self) -> str:
        """
        Возвращает строковое представление продукта.
        """
        return f"{self.name} ({self.model})"


class GridNode(models.Model):
    """
    Модель для хранения информации о звене сети, которое может быть заводом, розничной сетью или ИП.
    """
    FACTORY: int = 0
    RETAIL: int = 1
    ENTREPRENEUR: int = 2

    NODE_TYPES = (
        (FACTORY, "Завод"),
        (RETAIL, "Розничная сеть"),
        (ENTREPRENEUR, "ИП"),
    )

    title: str = models.CharField(max_length=100, verbose_name="Название звена")
    node_type: int = models.IntegerField(choices=NODE_TYPES, verbose_name="Тип звена")
    contact: NodeContact = models.OneToOneField(
        NodeContact, on_delete=models.CASCADE, verbose_name="Контакты"
    )
    products: models.ManyToManyField = models.ManyToManyField(EliteProduct, verbose_name="Продукты")
    supplier: Optional["GridNode"] = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
    )
    debt: models.DecimalField = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Задолженность",
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    employees: models.ManyToManyField = models.ManyToManyField(User, verbose_name="Сотрудники", blank=True)

    class Meta:
        verbose_name = "Звено EliteGrid"
        verbose_name_plural = "Звенья EliteGrid"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Возвращает строковое представление звена сети.
        """
        return f"{self.get_node_type_display()}: {self.title}"

    def save(self, *args, **kwargs) -> None:
        """
        Переопределенный метод save.
        Проверяет, что звено, кроме завода, должно иметь поставщика.
        """
        if not self.supplier and self.node_type != self.FACTORY:
            raise ValueError("Все звенья, кроме заводов, должны иметь поставщика")
        super().save(*args, **kwargs)
