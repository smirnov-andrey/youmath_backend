from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        IntegerField)

from materials.models import Article, Contact, Section, SubSection


class ArticleNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения работ."""
    class Meta:
        model = Article
        fields = ('id', 'title', 'subtitle')

class SectionNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения разделов."""
    class Meta:
        model = SubSection
        fields = ('id', 'title', 'subtitle')

class SubSectionNestedSerializer(ModelSerializer):
    """Вложенный сериализатор для отображения подразделов."""
    class Meta:
        model = SubSection
        fields = ('id', 'title', 'subtitle')


class ArticleSerializer(ModelSerializer):
    """Сериализатор для отображения работ."""
    section = SectionNestedSerializer()
    subsection = SubSectionNestedSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'subtitle', 'description', 'read_counter',
                  'file', 'section', 'subsection')


class SubSectionSerializer(ModelSerializer):
    """Сериализатор для отображения подразделов."""
    section = SectionNestedSerializer()
    articles_count = IntegerField()

    class Meta:
        model = SubSection
        fields = ('id', 'title', 'subtitle', 'description', 'read_counter',
                  'articles_count', 'section')


class SectionListSerializer(ModelSerializer):
    """Сериализатор для отображения списка всех разделов."""
    subsection_exist = SerializerMethodField()
    subsections_count = IntegerField()
    articles_count = IntegerField()

    class Meta:
        model = Section
        fields = ('id', 'title', 'subtitle', 'description', 'read_counter',
                  'subsection_exist', 'subsections_count', 'articles_count')

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
        fields = ('id', 'title', 'subtitle', 'description', 'read_counter',
                  'subsection_exist', 'subsections_count', 'articles_count',
                  'subsections', 'articles')
        read_only_fields = ('id', 'title', 'subtitle', 'description',
                            'read_counter',
                            'subsection_exist', 'subsections_count',
                            'articles_count', 'subsections', 'articles')

    def get_subsection_exist(self, obj):
        return bool(obj.subsections.count())

    def get_subsections(self, obj):
        return SubSectionNestedSerializer(
            obj.subsections.with_counters_annotated(),
            many=True
        ).data

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
        fields = ('id', 'title', 'subtitle', 'description', 'read_counter',
                  'subsection_exist', 'subsections_count', 'articles_count',
                  'popular_articles')

    def get_subsection_exist(self, obj):
        return bool(obj.subsections.count())

    def get_popular_articles(self, obj):
        return ArticleNestedSerializer(
            obj.articles.order_by('-read_counter')[:3],
            many=True
        ).data

class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact
        fields = ('email', 'name', 'message')
