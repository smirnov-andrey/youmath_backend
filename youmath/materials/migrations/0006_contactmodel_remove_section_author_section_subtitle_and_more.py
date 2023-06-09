# Generated by Django 4.1.7 on 2023-06-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_article_subtitle_section_author_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, verbose_name='Адрес электронной почты')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Имя')),
                ('message', models.CharField(blank=True, max_length=5000, verbose_name='Сообщение')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата обращения')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.RemoveField(
            model_name='section',
            name='author',
        ),
        migrations.AddField(
            model_name='section',
            name='subtitle',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Подзаголовок'),
        ),
        migrations.AddField(
            model_name='subsection',
            name='subtitle',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Подзаголовок'),
        ),
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Заголовок'),
        ),
    ]
