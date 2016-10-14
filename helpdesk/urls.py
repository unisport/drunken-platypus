from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.issueIndex, name='issue_index'),
    url(r'^(?P<issue_id>[0-9]+)/show/$', views.issueShow, name='issue_show'),
    url(r'^issue/new/$', views.issueCreate, name='issue_create'),
    url(r'^issue/(?P<issue_id>[0-9]+)/edit/$', views.issueEdit, name='issue_edit'),
    url(r'^issue/(?P<issue_id>[0-9]+)/comment/$', views.commentCreate, name='comment_create')
]