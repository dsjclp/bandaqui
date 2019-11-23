from . import views
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('post/list/', views.PostList.as_view(), name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]