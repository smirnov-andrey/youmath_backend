from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ArticleViewSet, ContactViewSet,
                    SectionViewSet, SubSectionViewSet)

app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register('articles',
                   ArticleViewSet,
                   basename='articles')
router_v1.register('contact',
                   ContactViewSet,
                   basename='contact')
router_v1.register('sections',
                   SectionViewSet,
                   basename='sections')
router_v1.register('subsections',
                   SubSectionViewSet,
                   basename='subsections')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
