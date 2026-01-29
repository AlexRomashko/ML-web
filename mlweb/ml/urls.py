from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='diplom'),
    path('download/<int:pk>/', views.download_file, name='download_file'),
    path('main', views.mainView, name='main')
]