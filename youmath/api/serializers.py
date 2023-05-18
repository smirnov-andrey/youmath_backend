from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        IntegerField)
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from materials.models import Section, SubSection, Article


class ArticleNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения работ."""
    class Meta:
        model = Article
        fields = ('id', 'title', 'subtitle', 'description', 'read_counter')


class SubSectionNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения подразделов."""
    class Meta:
        model = SubSection
        fields = ('id', 'title', 'description', 'read_counter')


class ArticleSerializer(ModelSerializer):
    """Сериализатор для отображения работ."""
    class Meta:
        model = Article
        fields = ('id', 'title', 'subtitle', 'description', 'read_counter',
                  'file')


class SectionListSerializer(ModelSerializer):
    """Сериализатор для отображения списка всех разделов."""
    subsection_exist = SerializerMethodField()
    subsections_count = IntegerField()
    articles_count = IntegerField()

    class Meta:
        model = Section
        fields = ('id', 'title', 'author', 'description', 'read_counter',
                  'subsection_exist', 'subsections_count', 'articles_count')

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_subsection_exist(self, obj):
        return bool(obj.subsections.count())


class SectionDetailSerializer(ModelSerializer):
    """Сериализатор для отображения деталей раздела с подразделами и
    работами."""
    subsection_exist = SerializerMethodField(read_only=True)
    subsections_count = IntegerField(read_only=True)
    articles_count = IntegerField(read_only=True)
    subsections = SerializerMethodField(read_only=True)
    articles = SerializerMethodField(read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'title', 'author', 'description', 'read_counter',
                  'subsection_exist', 'subsections_count', 'articles_count',
                  'subsections', 'articles')
        read_only_fields = ('id', 'title', 'author', 'description',
                            'read_counter',
                            'subsection_exist', 'subsections_count',
                            'articles_count', 'subsections', 'articles')

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_subsection_exist(self, obj):
        return bool(obj.subsections.count())

    @extend_schema_field(SubSectionNestedSerializer(many=True))
    def get_subsections(self, obj):
        return SubSectionNestedSerializer(
            obj.subsections,
            many=True
        ).data

    @extend_schema_field(ArticleNestedSerializer(many=True))
    def get_articles(self, obj):
        return ArticleNestedSerializer(
            obj.articles,
            many=True
        ).data


class PopularSectionSerializer(ModelSerializer):
    """Сериализатор для отображения популярных разделов."""
    subsection_exist = SerializerMethodField()
    popular_articles = SerializerMethodField()
    subsections_count = IntegerField()
    articles_count = IntegerField()

    class Meta:
        model = Section
        fields = ('id', 'title', 'author', 'description', 'read_counter',
                  'subsection_exist', 'subsections_count', 'articles_count',
                  'popular_articles')

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_subsection_exist(self, obj):
        return bool(obj.subsections.count())

    @extend_schema_field(ArticleNestedSerializer(many=True))
    def get_popular_articles(self, obj):
        return ArticleNestedSerializer(
            obj.articles.order_by('-read_counter')[:3],
            many=True
        ).data


class SubSectionSerializer(ModelSerializer):
    """Сериализатор для отображения подразделов."""
    articles_count = IntegerField()

    class Meta:
        model = SubSection
        fields = ('id', 'title', 'description', 'read_counter',
                  'articles_count')
