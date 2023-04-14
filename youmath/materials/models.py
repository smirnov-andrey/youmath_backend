from django.db import models

from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
def article_directory_path(instance, filename):
    filebase, extention = filename.split('.')
    if instance.subsection:
        return (f'articles/{instance.section.id}'
                f'/{instance.subsection.id}/'
                f'{instance.slug}.{extention}')
    else:
        return (f'articles/{instance.section.id}/'
                f'{instance.slug}.{extention}')


class Section(models.Model):
    """Модель разделов работ"""
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Уникальный слаг',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    read_counter = models.PositiveBigIntegerField(
        default=0,
        blank=False,
        verbose_name='Просмотров'
    )
    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано'
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'раздел'
        verbose_name_plural = 'Разделы'


class SubSection(models.Model):
    """Модель подразделов работ"""
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Уникальный слаг',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    read_counter = models.PositiveBigIntegerField(
        default=0,
        blank=False,
        verbose_name='Просмотров'
    )
    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано'
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='Дата обновления'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        null=False,
        verbose_name='Раздел',
        related_name='subsections'
    )

    def __str__(self):
        return self.title
            # f'{self.title} (раздел: {self.section.title})'

    class Meta:
        ordering = ('title',)
        verbose_name = 'подраздел'
        verbose_name_plural = 'Подразделы'


class Article(models.Model):
    """Модель работ / статей"""
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Уникальный слаг',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    read_counter = models.PositiveBigIntegerField(
        default=0,
        blank=False,
        verbose_name='Просмотров'
    )
    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано'
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    updated = models.DateTimeField(
        auto_now=True,
        auto_now_add=False,
        verbose_name='Дата обновления'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        null=False,
        verbose_name='Раздел',
        related_name='articles'
    )
    subsection = ChainedForeignKey(
        SubSection,
        chained_field="section",
        chained_model_field="section",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Подраздел',
        related_name='articles'
    )

    # subsection = models.ForeignKey(
    #     SubSection,
    #     on_delete=models.PROTECT,
    #     null=True,
    #     verbose_name='Подраздел',
    #     related_name='articles'

    # todo: add file extention validation
    file = models.FileField(
        upload_to=article_directory_path,
        null=True,
        blank=True,
        verbose_name='Файл работы'
    )
    content = models.TextField(
        null=True,
        blank=True,
        verbose_name='LanTeX / MathML',
    )
    is_converted = models.BooleanField(
        default=False,
        blank=False,
        verbose_name='Сконвертировано',
    )

    def __str__(self):
        return self.title

    class Meta:

        verbose_name = 'работа'
        verbose_name_plural = 'Работы'