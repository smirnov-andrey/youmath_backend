from rest_framework.serializers import ModelSerializer, SerializerMethodField
from drf_spectacular.utils import extend_schema_field

from materials.models import Section, SubSection, Article


class ArticleNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения работ."""
    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'read_counter')


class SectionNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения разделов."""
    class Meta:
        model = Section
        fields = ('id', 'title', 'description', 'read_counter')


class SubSectionNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения подразделов."""
    class Meta:
        model = SubSection
        fields = ('id', 'title', 'description', 'read_counter')


class ArticleSerializer(ModelSerializer):
    """Сериализатор для отображения работ."""
    section = SectionNestedSerializer(many=False, read_only=True)
    subsection = SubSectionNestedSerializer(many=False, read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'description', 'read_counter', 'file',
                  'section', 'subsection')


class SectionSerializer(ModelSerializer):
    """Сериализатор для отображения разделов."""
    subsection_exist = SerializerMethodField()
    popular_subsections = SerializerMethodField()
    popular_articles = SerializerMethodField()

    class Meta:
        model = Section
        fields = ('id', 'title', 'description', 'read_counter',
                  'subsection_exist', 'popular_subsections',
                  'popular_articles')

    def get_subsection_exist(self, obj):
        return bool(
            obj.subsections.count()
        )

    @extend_schema_field(SubSectionNestedSerializer(many=True))
    def get_popular_subsections(self, obj):
        return SubSectionNestedSerializer(
            obj.subsections.order_by('-read_counter')[:10],
            many=True
        ).data

    @extend_schema_field(ArticleNestedSerializer(many=True))
    def get_popular_articles(self, obj):
        return ArticleNestedSerializer(
            obj.articles.order_by('-read_counter')[:10],
            many=True
        ).data


class SubSectionSerializer(ModelSerializer):
    """Сериализатор для отображения подразделов."""
    popular_articles = SerializerMethodField()

    class Meta:
        model = SubSection
        fields = ('id', 'title', 'description', 'read_counter',
                  'popular_articles')

    @extend_schema_field(ArticleNestedSerializer(many=True))
    def get_popular_articles(self, obj):
        return ArticleNestedSerializer(
            obj.articles.order_by('-read_counter')[:10],
            many=True
        ).data
