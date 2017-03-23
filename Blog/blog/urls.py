from django.conf.urls import url
from . import views



urlpatterns = [
            url(r'^$',views.indexview,name="indexview"),
            url(r'^index/$',views.indexview,name="indexview"),
            url(r'^details/(?P<article_id>[0-9]+)/$',views.detailsview,name="details"),
            url(r'^login/$',views.loginview,name="login"),
            url(r'^regist/$',views.registview,name="regist"),
            url(r'^logout/$',views.logoutview,name="logout"),
            url(r'^master/(?P<master_id>[0-9]+)/$',views.masterview,name="master"),
            url(r'^event/$',views.eventview,name="event"),
            url(r'^event/(?P<event_id>[0-9]+)/$',views.eventdetailview,name="eventdetail"),
]
