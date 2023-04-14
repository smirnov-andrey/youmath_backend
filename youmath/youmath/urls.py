"""youmath URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

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
    path('api/', include('api.urls')),
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$',
    #         schema_view.without_ui(cache_timeout=0),
    #         name='schema-json'),
    # re_path(r'^swagger/$',
    #         schema_view.with_ui('swagger', cache_timeout=0),
    #         name='schema-swagger-ui'),
    # re_path(r'^redoc/$',
    #         schema_view.with_ui('redoc', cache_timeout=0),
    #         name='schema-redoc'),

    path('schema/',
         SpectacularAPIView.as_view(),
         name='schema'),
    # Optional UI:
    path('swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('redoc/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
    # path('api/schema/',
    #      SpectacularAPIView.as_view(),
    #      name='schema'),
    # # Optional UI:
    # path('api/schema/swagger-ui/',
    #      SpectacularSwaggerView.as_view(url_name='schema'),
    #      name='swagger-ui'),
    # path('api/schema/redoc/',
    #      SpectacularRedocView.as_view(url_name='schema'),
    #      name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
