from django.urls import include, path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

#app_name = 'core'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('info', views.InfoPage.as_view(), name='info'),
    path('memberhome', views.MemberhomePage.as_view(), name='memberhome'),
    path('photo', views.PhotoListView.as_view(), name='photo'),
    path('video', views.VideoListView.as_view(), name='video'),
    path('accounts', include('django.contrib.auth.urls')),
    path('events.json', views.events_json, name='events.json'),
]
