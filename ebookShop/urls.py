from django.conf.urls import url

from . import views

app_name = 'ebookShop'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^book/$', views.book, name='book'),
    url(r'^cat/$', views.category, name='category'),
    url(r'^addBasket/$', views.addBasket, name='addBasket'),
    url(r'^removeBasket/$', views.removeBasket, name='removeBasket'),
    url(r'^basket/$', views.showBasket, name='showBasket'),
    url(r'^orders/$', views.showOrders, name='showOrders'),
]
