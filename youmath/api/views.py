from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (ArticleSerializer,
                          ContactSerializer,
                          PopularSectionSerializer,
                          SectionListSerializer,
                          SectionDetailSerializer,
                          SubSectionSerializer)
from materials.models import Contact, Section, SubSection, Article


class SectionViewSet(ListModelMixin, GenericViewSet):
    queryset = Section.objects.with_counters_annotated()
    serializer_class = SectionListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ('id', 'title', 'subtitle', 'slug', 'description',
                       'read_counter')
    search_fields = ('title', 'subtitle', 'slug', 'description')

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(
            Section.objects.with_counters_annotated(),
            pk=pk
        )
        queryset.read_counter += 1
        queryset.save()
        serializer = SectionDetailSerializer(queryset)
        return Response(serializer.data)

    @action(
        methods=['GET'],
        detail=False,
        url_path=r'popular',
        url_name='popular')
    def popular(self, request):
        queryset = self.filter_queryset(self.get_queryset()).order_by(
            '-read_counter')[:10]
        serializer = PopularSectionSerializer(queryset, many=True)
        return Response(serializer.data)


class SubSectionViewSet(ListModelMixin, GenericViewSet):
    queryset = SubSection.objects.with_counters_annotated().select_related(
        'section')
    serializer_class = SubSectionSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('section',)
    ordering_fields = ('id', 'title', 'subtitle', 'slug', 'description',
                       'read_counter')
    search_fields = ('title', 'subtitle', 'slug', 'description')

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(
            SubSection.objects.with_counters_annotated(),
            pk=pk
        )
        queryset.read_counter += 1
        queryset.save()
        serializer = SubSectionSerializer(queryset)
        return Response(serializer.data)

    # @action(
    #     methods=['GET'],
    #     detail=False,
    #     url_path=r'popular',
    #     url_name='popular')
    # def popular(self, request):
    #     queryset = self.filter_queryset(self.get_queryset()).order_by(
    #         '-read_counter')[:3]
    #     serializer = PopularSubSectionSerializer(queryset, many=True)
    #     return Response(serializer.data)


class ArticleViewSet(ListModelMixin, GenericViewSet):
    queryset = Article.objects.all().select_related(
        'section', 'subsection')
    serializer_class = ArticleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('section', 'subsection')
    ordering_fields = ('id', 'title', 'subtitle', 'slug', 'description',
                       'read_counter')
    search_fields = ('title', 'subtitle', 'slug', 'description', 'content')

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Article.objects.all(), pk=pk)
        queryset.read_counter += 1
        queryset.save()
        serializer = ArticleSerializer(queryset)
        return Response(serializer.data)

    # @action(
    #     methods=['GET'],
    #     detail=False,
    #     url_path=r'popular',
    #     url_name='popular',
    # )
    # def popular(self, request):
    #     queryset = self.filter_queryset(self.get_queryset()).order_by(
    #         '-read_counter')[:10]
    #     serializer = ArticleSerializer(queryset, many=True)
    #     return Response(serializer.data)


class ContactViewSet(CreateModelMixin, GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
