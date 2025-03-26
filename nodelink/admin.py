from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpRequest
from typing import Optional
from django.db.models import QuerySet
from .models import EliteProduct, GridNode, NodeContact


class ContactInline(admin.StackedInline):
    """
    Inline форма для отображения и редактирования контактной информации в админке.
    Модель связана с NodeContact, позволяет добавить новый контакт для узла.

    Attributes:
        model: Модель NodeContact для отображения в форме.
        extra: Количество пустых форм для добавления новых контактов (по умолчанию 1).
    """
    model = NodeContact
    extra: int = 1


class ProductInline(admin.TabularInline):
    """
    Inline форма для отображения и редактирования продуктов, связанных с GridNode.
    Связывает GridNode и EliteProduct через промежуточную таблицу.

    Attributes:
        model: Промежуточная модель для связи продуктов с узлом.
        extra: Количество пустых форм для добавления новых продуктов (по умолчанию 1).
    """
    model = GridNode.products.through
    extra: int = 1


@admin.register(GridNode)
class GridNodeAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели GridNode. Отображает и редактирует данные о звене сети,
    включая название, тип звена, задолженность перед поставщиком, связанные продукты и контакты.

    Атрибуты:
        list_display: Поля для отображения в списке объектов в админке.
        list_filter: Фильтры для сортировки и поиска в админке.
        inlines: Встроенные формы для редактирования связанных моделей (контактов и продуктов).
        exclude: Поля, которые не будут отображаться в форме редактирования объекта.
        actions: Действия, доступные для выбора и изменения данных в списке объектов.
    """
    list_display: tuple = ("title", "node_type_display", "supplier_link", "debt", "created_at")
    list_filter: tuple = ("contact__city", "node_type", "contact__country", "debt")
    inlines: list = [ContactInline, ProductInline]
    exclude: tuple = ("products",)
    actions: list = ["clear_debt"]

    def node_type_display(self, obj: GridNode) -> str:
        """
        Отображает тип звена (например, "Завод", "Розничная сеть", "ИП") в виде строки.

        Аргументы:
            obj: Экземпляр GridNode.

        Возвращаемое значение:
            Строка с отображаемым типом звена.
        """
        return obj.get_node_type_display()

    node_type_display.short_description: str = "Тип звена"

    def supplier_link(self, obj: GridNode) -> str:
        """
        Отображает ссылку на поставщика для данного узла (если поставщик существует).

        Аргументы:
            obj: Экземпляр GridNode.

        Возвращаемое значение:
            Ссылка на страницу поставщика в админке или знак "-" если поставщик не указан.
        """
        if obj.supplier:
            return format_html(
                '<a href="{}">{}</a>',
                f"/admin/NodeLink/gridnode/{obj.supplier.id}/change/",
                obj.supplier.title,
            )
        return "-"

    supplier_link.short_description: str = "Поставщик"

    def clear_debt(self, request: HttpRequest, queryset: QuerySet) -> None:
        """
        Действие для обнуления задолженности у выбранных узлов. Если фильтр по типу узла
        установлен на "Розничная сеть", задолженность будет обнулена только для этих узлов.

        Аргументы:
            request: Запрос, содержащий информацию о выбранных объектах и фильтрах.
            queryset: Список выбранных объектов для обновления.

        Возвращаемое значение:
            Нет.
        """
        node_type: Optional[str] = request.GET.get("node_type")

        if node_type == str(GridNode.RETAIL):
            # Обнуляем задолженность только для узлов с типом "Розничная сеть"
            queryset.filter(node_type=GridNode.RETAIL).update(debt=0)
        else:
            # Обнуляем задолженность для всех выбранных узлов
            queryset.update(debt=0)

    clear_debt.short_description: str = "Обнулить задолженность"


@admin.register(EliteProduct)
class EliteProductAdmin(admin.ModelAdmin):
    """
    Админ-панель для модели EliteProduct. Отображает информацию о продукте с его названием,
    моделью и датой выхода на рынок.

    Атрибуты:
        list_display: Поля для отображения в списке объектов в админке.
    """
    list_display: tuple = ("name", "model", "release_date")


admin.site.register(NodeContact)
