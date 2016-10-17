from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.issue_index, name='issue_index'),
    url(r'^(?P<issue_id>[0-9]+)/show/$', views.issue_show, name='issue_show'),
    url(r'^issue/new/$', views.issue_create, name='issue_create'),
    url(r'^issue/(?P<issue_id>[0-9]+)/edit/$', views.issue_edit, name='issue_edit'),
    url(r'^issue/(?P<issue_id>[0-9]+)/comment/$', views.comment_create, name='comment_create'),
    url(r'^changelog/new/$', views.changelog_new, name='changelog_new'),
    url(r'^kb/new/$', views.article_new, name='article_new'),
    url(r'^kb/$', views.article_index, name='article_index'),
    url(r'^kb/(?P<article_id>[0-9]+)/$', views.article_show, name='article_show'),
    url(r'^kb/(?P<article_id>[0-9]+)/edit/$', views.article_exit, name='article_exit'),
]