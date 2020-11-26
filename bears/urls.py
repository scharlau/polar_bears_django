from django.urls import path
from . import views

urlpatterns = [
        path('', views.bear_list, name='bear_list'),
        path('bear/<int:id>/', views.bear_detail, name= 'bear_detail'),
        ]