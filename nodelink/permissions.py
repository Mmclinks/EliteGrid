from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsActiveEmployee(BasePermission):
    """
    Права доступа для проверки, является ли пользователь активным.
    Разрешает доступ только активным сотрудникам.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        """
        Проверяет, является ли пользователь активным.

        :param request: Запрос, содержащий пользователя.
        :param view: Представление, к которому осуществляется запрос.
        :return: True, если пользователь активен, иначе False.
        """
        return bool(request.user and request.user.is_active)
