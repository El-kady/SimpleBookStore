from django.db import models
from django.utils.timezone import datetime
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from math import ceil


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='received_notifications')
    book = models.ForeignKey('Book', null=True)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ['-created_at']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='ProfileCategory', related_name='followed_by')
    authors = models.ManyToManyField('Author', through='ProfileAuthor', related_name='followed_by')
    books = models.ManyToManyField('Book', through='ProfileBook', related_name='user_by')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ProfileCategory(models.Model):
    category = models.ForeignKey('Category')
    profile = models.ForeignKey('Profile')
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(default=datetime.now)


class ProfileAuthor(models.Model):
    author = models.ForeignKey('Author')
    profile = models.ForeignKey('Profile')
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(default=datetime.now)


class ProfileBook(models.Model):
    book = models.ForeignKey('Book')
    profile = models.ForeignKey('Profile')
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(default=datetime.now)


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
    created_at = models.DateTimeField(default=datetime.now)

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

    class Meta:
        ordering = ['-id']


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
            return '/static/SimpleBookStore/images/avatar.png'
