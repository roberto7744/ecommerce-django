from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import index
from store import create_admin


schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce API",
        default_version="v1",
        description="Documentación de la API del proyecto Ecommerce",
        contact=openapi.Contact(email="roberto@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", index, name="home"),
    path("admin/", admin.site.urls),

    # API principal
    path("api/", include("store.urls")),

    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("openapi.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]
