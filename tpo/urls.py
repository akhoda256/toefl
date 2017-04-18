from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	# ex: /evals/upload/
    url(r'^reading/$', views.reading, name='reading'),
    url(r'^(?P<tpoNumber>[0-9]{1}/)passage/(?P<passageNumber>[0-9]{1}/)$', views.passageText, name='passage'),
]