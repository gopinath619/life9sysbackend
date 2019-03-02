from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns=[
    url('^signup/$',teachersignup),
    url(r'^loginusers',login_user),
    url(r'^logoutuser',logout),
    url(r'^newcourse', addnewcourse),
    url(r'^getcourses', getallcourses),
    url(r'^newchapters', addnewchapter),
    url(r'^getchapters', getchapters),
    url(r'^newtopic', addnewtopic),
    url(r'^gettopics', gettopics),

]