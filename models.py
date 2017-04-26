from django.db import models
from django.utils.timezone import datetime
from django.db.models import Count
from math import ceil

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.ForeignKey('Category', related_name='books')
    author = models.ForeignKey('Author', related_name='books')
    cover = models.ImageField(upload_to='uploads/books/covers/')

    def __str__(self):
        return self.title

    def rating(self):
        rating_totals = self.vote_set.all().values('value').annotate(total=Count('id')).order_by('total')
        _total = 0
        _sum = 0
        _rating = 0
        for rating in rating_totals:
            _total = _total + rating.get('total')
            _sum = _sum + (rating.get('total') * rating.get('value'))

        if _total > 0:
            _rating = _sum / _total

        return ceil(_rating)


class Vote(models.Model):
    book = models.ForeignKey('Book')
    user = models.ForeignKey('auth.User')
    value = models.SmallIntegerField()
    created_at = models.DateTimeField(default=datetime.now)


class Author(models.Model):
    name = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='uploads/books/photos/', blank=True)
    birthdate = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name

    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return 'static/SimpleBookStore/images/avatar.png'
