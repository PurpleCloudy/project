from distutils.command.upload import upload
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
import os
from PIL import Image
from io import BytesIO

# Create your models here.
User = settings.AUTH_USER_MODEL

ANSWERS = [
    ('yes', 'есть в библиотеке'),
    ('no', 'нет в библиотеке')
]

TAGS = [
    ('FAN','фэнтези'),
    ('STU','учебники'),
    ('FIC','научная фантастика'),
    ('SCI','научная литература'),
    ('DIC','словари, справочники и тд'),
]

QUALITY = [
    ('VBA','книга испорчена'),
    ('BAD','ветхая, будьте осторожны'),
    ('NOR','неплохая, но уже не новая'),
    ('ANE','почти новая'),
    ('NEW','новая'),
]

class Comments(models.Model):
    class Meta:
        ordering = ['-date']
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False, null=True)

class Likes(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    like = models.BooleanField(default=False)

class News(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    author_book = models.CharField(verbose_name="Имя автора",max_length=100, default='Не указан')
    article = models.CharField(verbose_name="Название книги",max_length=100)
    body = models.TextField(verbose_name="Описание", blank = True, null = True)
    commentary = models.ManyToManyField(Comments)
    likes = models.ManyToManyField(Likes)
    image = models.ImageField(verbose_name="Обложка", upload_to = 'news_images/', default = 'news_images/default_news.jpg')
    image_thumbnail = models.ImageField(upload_to = 'news_images/', null = True, blank = True)
    tag = models.CharField(verbose_name='Тег', choices=TAGS, max_length=3, default='STU')
    quality = models.CharField(verbose_name='Качество книги', choices=QUALITY, max_length=3, default='NOR')
    is_in = models.CharField(verbose_name='Наличие книги', choices=ANSWERS, max_length=30, default='yes')

    def __str__(self):
        return self.article

    def get_likes(self):
        print(self.likes.count())
        return self.likes.count()
    
    def get_image_name(self):
        print(1)
        if self.image:
            return self.image.name
        else:
            return False

    def make_thumbnail(self):
        image = Image.open(self.image)
        image.thumbnail((200, 200), Image.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name.split('/')[0] + '_thumb' + thumb_extension
        image_thumbnail = models.ImageField(
            upload_to='news_images/',
            default='news_images/default_news.jpg',
            null=True,
            blank=True
        )

        if thumb_name == 'news_images/default_news.jpg':
            return

        if thumb_extension in ['.jpg', '.jpeg']:
            FILE_TYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FILE_TYPE = 'GIF'
        elif thumb_extension == '.png':
            FILE_TYPE = 'PNG'
        temp_thumb = BytesIO()
        image.save(temp_thumb, FILE_TYPE)
        temp_thumb.seek(0)
        self.image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save = False)
        temp_thumb.close()
        
    def save(self, *args, **kwargs):
        self.make_thumbnail()
        super(News, self).save(*args, **kwargs)


        