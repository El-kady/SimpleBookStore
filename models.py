from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=120)

class Book(models.Model):
    title = models.CharField(max_length=120)
    category = models.ForeignKey('Category', related_name='books')
    author = models.ForeignKey('Author', related_name='books')

class Author(models.Model):
    name = models.CharField(max_length=120)