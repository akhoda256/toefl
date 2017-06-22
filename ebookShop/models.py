from django.db import models


class Category(models.Model):
    name = models.TextField(max_length=50)

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


class Book(models.Model):
    title = models.TextField(max_length=50)
    description = models.TextField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, default=None)
    coverPhoto = models.ImageField(upload_to='ebookShop/static/img')
    category = models.ForeignKey(Category, default=None)

    def __str__(self):
        return str(self.title)

