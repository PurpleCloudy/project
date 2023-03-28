# Generated by Django 4.1.3 on 2023-03-28 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_news_quality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='quality',
            field=models.CharField(choices=[('книга испорчена', 'книга испорчена'), ('ветхая, будьте осторожны', 'ветхая, будьте осторожны'), ('неплохая, но уже не новая', 'неплохая, но уже не новая'), ('почти новая', 'почти новая'), ('новая', 'новая')], default='NOR', max_length=30, verbose_name='качество книги'),
        ),
    ]