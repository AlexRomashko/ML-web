from django.urls import path
from . import views


urlpatterns = [
    path('one_exp', views.process_data, name='one_exp'),
    path('process_data/', views.process_data, name='process_data'),
    path('download_csv/<str:file_name>/', views.download_csv, name='download_csv'),
]