# Generated by Django 4.1.7 on 2023-04-11 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_alter_article_section_alter_article_subsection_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ('title',), 'verbose_name': 'раздел', 'verbose_name_plural': 'Разделы'},
        ),
        migrations.AlterModelOptions(
            name='subsection',
            options={'ordering': ('title',), 'verbose_name': 'подраздел', 'verbose_name_plural': 'Подразделы'},
        ),
        migrations.AlterField(
            model_name='article',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articles', to='materials.section', verbose_name='Раздел'),
        ),
        migrations.AlterField(
            model_name='article',
            name='subsection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='articles', to='materials.subsection', verbose_name='Подраздел'),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subsections', to='materials.section', verbose_name='Раздел'),
        ),
    ]
