from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	# ex: /evals/upload/
    url(r'^reading/$', views.reading, name='reading')
]