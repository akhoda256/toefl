from django.conf.urls import url

from . import views

app_name = 'ebookShop'
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^book/$', views.book, name='book')
]
