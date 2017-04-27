from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reading/$', views.reading, name='reading'),
    url(r'^passage/?$', views.passageText, name='passage'),
    # url(r'^ajax/getQuestion/$', views.getQuestion, name='getQuestion'),
    url(r'^passage/question/$', views.getReadingQuestion, name='getQuestion'),
    # url(r'^q/$', views.getQuestion, name='pgetQuestion')
    url(r'^listening/?$', views.listeningAudio, name='conversation'),
    url(r'^listening/question/$', views.listeningQuestion, name='listeningQuestion'),
    url(r'^speaking/question/$', views.speakingQuestion, name='test'),
    url(r'^salam/$', views.salam, name='salam'),
]