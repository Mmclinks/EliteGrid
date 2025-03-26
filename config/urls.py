from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from nodelink.views import GridNodeViewSet

# Регистрируем маршруты для GridNodeViewSet
router = DefaultRouter()
router.register(r"nodes", GridNodeViewSet)

urlpatterns = [
    # Админка Django
    path('admin/', admin.site.urls),

    # JWT авторизация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API для работы с узлами
    path('api/', include(router.urls)),
]
