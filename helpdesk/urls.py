from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.issue_index, name='issue_index'),
    url(r'^(?P<issue_id>[0-9]+)/show/$', views.issue_show, name='issue_show'),
    url(r'^issue/new/$', views.issue_create, name='issue_create'),
    url(r'^issue/(?P<issue_id>[0-9]+)/edit/$', views.issue_edit, name='issue_edit'),
    url(r'^issue/(?P<issue_id>[0-9]+)/comment/$', views.comment_create, name='comment_create')
]