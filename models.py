from django.db import models
from django.utils.timezone import datetime


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=120)
    category = models.ForeignKey('Category', related_name='books')
    author = models.ForeignKey('Author', related_name='books')
    cover = models.ImageField(upload_to='uploads/books/covers/')

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='uploads/books/photos/',blank=True)
    birthdate = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name

    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return 'static/SimpleBookStore/images/avatar.png'

