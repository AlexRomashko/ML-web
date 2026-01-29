from django.urls import path
from . import views


urlpatterns = [
    path('linear', views.pca, name='linear'),
    path('process_pca/', views.pca, name='process_pca')
]