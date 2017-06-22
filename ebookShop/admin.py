from django.contrib import admin
from ebookShop.models import Book, Publication , Author , Category
# Register your models here.

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Publication)
admin.site.register(Author)

