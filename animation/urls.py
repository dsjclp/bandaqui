
from django.urls import path
from . import views
from django.views.static import serve
from django.conf.urls import url


app_name = 'animation'

urlpatterns = [
    path('event/<int:id>', views.eventdetail, name='eventdetail'),
    path('eventprogram/<int:id>/', views.eventprogram, name='eventprogram'),
    path('pieces/', views.PieceListView.as_view(), name='pieces'),
    path("participation/create/<int:id>/", views.participation_create, name='participation_create'),
]