# Generated by Django 4.1.3 on 2023-03-27 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_news_tags_news_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='author_book',
            field=models.CharField(default='Не указан', max_length=100, verbose_name='Имя автора'),
        ),
    ]
