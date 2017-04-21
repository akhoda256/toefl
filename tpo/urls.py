from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	# ex: /evals/upload/
    url(r'^reading/$', views.reading, name='reading'),
    url(r'^p/$', views.passageText, name='passage'),
    # url(r'^ajax/getQuestion/$', views.getQuestion, name='getQuestion'),
    url(r'^q/$', views.getQuestion, name='getQuestion'),
    # url(r'^q/$', views.getQuestion, name='pgetQuestion')
    url(r'^l/$', views.listeningAudio, name='conversation'),
]