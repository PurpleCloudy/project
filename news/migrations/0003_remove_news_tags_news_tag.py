# Generated by Django 4.1.3 on 2023-03-25 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_tags_alter_news_article_alter_news_body_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='tags',
        ),
        migrations.AddField(
            model_name='news',
            name='tag',
            field=models.CharField(choices=[('FAN', 'фэнтези'), ('STU', 'учебники'), ('FIC', 'научная фантастика'), ('SCI', 'научная литература'), ('DIC', 'словари, справочники и тд')], default='STU', max_length=3, verbose_name='тег'),
        ),
    ]
