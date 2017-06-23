from django.contrib import admin
from ebookShop.models import Book, Publication , Author , Category, Format

# Register your models here.

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Publication)
admin.site.register(Author)
admin.site.register(Format)
