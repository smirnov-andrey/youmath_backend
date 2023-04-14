from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import (SectionSerializer,
                          SubSectionSerializer,
                          ArticleSerializer)
from materials.models import Section, SubSection, Article


class SectionViewSet(ListModelMixin, GenericViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('id', 'title', 'slug', 'description',
                       'read_counter')

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Section.objects.all(), pk=pk)
        queryset.read_counter += 1
        queryset.save()
        serializer = SectionSerializer(queryset)
        return Response(serializer.data)

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'popular',
        url_name='popular')
    def popular(self, request):
        queryset = self.filter_queryset(self.get_queryset()).order_by(
            '-read_counter')[:10]
        serializer = SectionSerializer(queryset, many=True)
        return Response(serializer.data)


class SubSectionViewSet(ListModelMixin, GenericViewSet):
    serializer_class = SubSectionSerializer
    queryset = SubSection.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('section',)
    ordering_fields = ('id', 'title', 'slug', 'description',
                       'read_counter')

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(SubSection.objects.all(), pk=pk)
        queryset.read_counter += 1
        queryset.save()
        serializer = SubSectionSerializer(queryset)
        return Response(serializer.data)

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'popular',
        url_name='popular')
    def popular(self, request):
        queryset = self.filter_queryset(self.get_queryset()).order_by(
            '-read_counter')[:10]
        serializer = SubSectionSerializer(queryset, many=True)
        return Response(serializer.data)


class ArticleViewSet(ListModelMixin, GenericViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('section', 'subsection')
    ordering_fields = ('id', 'title', 'slug', 'description',
                       'read_counter')
    search_fields = ('title', 'slug', 'description', 'content',
                     'section__title', 'section__description',
                     'subsection__title', 'subsection__description')

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Article.objects.all(), pk=pk)
        queryset.read_counter += 1
        queryset.save()
        serializer = ArticleSerializer(queryset)
        return Response(serializer.data)

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'popular',
        url_name='popular',
    )
    def popular(self, request):
        queryset = self.filter_queryset(self.get_queryset()).order_by(
            '-read_counter')[:10]
        serializer = ArticleSerializer(queryset, many=True)
        return Response(serializer.data)
