from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.addForm, name='addForm'),
    path('add/content/', views.addCon, name='addCon'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.editCon, name='edit'),
    path('<int:pk>/edited/', views.editedCon , name='edited'),
]