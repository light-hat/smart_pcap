"""
Модyль, определяющий доступные url-адреса для сервиса.
"""

from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r"city", CityViewSet, basename="city")
# router.register(r"street", StreetViewSet, basename="street")
# router.register(r"shop", ShopViewSet, basename="shop")

urlpatterns = [
    path("", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
]
