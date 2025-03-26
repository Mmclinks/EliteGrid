from rest_framework import viewsets
from .models import GridNode
from .permissions import IsActiveEmployee  # Кастомное право доступа
from .serializers import GridNodeSerializer


class GridNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с узлами сети (GridNode).
    Реализует полный набор действий (CRUD) для работы с объектами модели GridNode.
    """
    queryset = GridNode.objects.all()
    serializer_class = GridNodeSerializer
    permission_classes = [IsActiveEmployee]  # Применяем кастомные права доступа

    def get_queryset(self):
        """
        Переопределенный метод для фильтрации по стране через параметры запроса.
        Если передан параметр 'country', фильтрует по соответствующему полю.
        """
        queryset = super().get_queryset()  # Получаем базовый queryset
        country = self.request.query_params.get("country")  # Параметр запроса 'country'

        if country:
            # Фильтруем по стране, если параметр есть в запросе
            queryset = queryset.filter(contact__country=country)

        return queryset
