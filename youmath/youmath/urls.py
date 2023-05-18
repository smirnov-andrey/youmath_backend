from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularRedocView,
                                   SpectacularSwaggerView)

schema_view = get_schema_view(
   openapi.Info(
      title="Youmath.ru API",
      default_version='v1',
      description="API documentation for youmath.ru project",
      # terms_of_service="https://www.google.com/policies/terms/",
      # contact=openapi.Contact(email="contact@snippets.local"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # todo: change to path
    re_path(r'^chaining/', include('smart_selects.urls')),
    path('api/', include('api.urls')),
    # path(
    #     'api/schema/',
    #     SpectacularAPIView.as_view(),
    #     name='schema'
    # ),
    # path(
    #     'api/swagger/',
    #     SpectacularSwaggerView.as_view(url_name='schema'),
    #     name='swagger-ui'
    # ),
    # path(
    #     'api/redoc/',
    #     SpectacularRedocView.as_view(url_name='schema'),
    #     name='redoc'
    # ),

    path('swagger/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
