from django.db import models

from toefl.settings import MEDIA_URL


class Category(models.Model):
    name = models.TextField(max_length=50)
    smallPhoto = models.ImageField(upload_to='img', null=True)
    bigPhoto = models.ImageField(upload_to='img', null=True)

    def __str__(self):
        return str(self.name)


class Author(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return str(self.name)


class Publication(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return str(self.name)


class Format(models.Model):
    name = models.TextField(max_length=50)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=2000)
    details = models.TextField(max_length=2000, default=None, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, default=None, null=True)
    coverPhoto = models.ImageField(upload_to='img')
    category = models.ForeignKey(Category, default=None, null=True)
    price = models.FloatField(default=0)
    format = models.ForeignKey(Format, default=None, null=True)
    onSale = models.BooleanField(default=False)
    fav = models.BooleanField(default=False)
    new = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    @property
    def get_absolute_image_url(self):
        return self.coverPhoto.url
