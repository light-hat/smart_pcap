"""
Конфигурация URL-адресов всего проекта.
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views import View
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


class SPAView(View):
    """
    Отображение фронтэнда.
    """

    def get(self, request, *args, **kwargs):
        """
        GET запрос для бандла.
        """
        index_file = os.path.join(settings.STATIC_ROOT, "index.html")
        if os.path.exists(index_file):
            with open(index_file, "rb") as f:
                return HttpResponse(f.read(), content_type="text/html")
        raise Http404("index.html not found in STATIC_ROOT")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("ids.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    re_path(r"^(?!api|admin).*", SPAView.as_view(), name="spa"),
]
