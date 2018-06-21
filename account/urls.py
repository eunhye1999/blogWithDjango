from django.urls import path
from . import views
# from django.contrib.auth.views import login, logout

app_name = 'account'
urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # path('login/', login, { 'template_name':'accouts/login.html' }),
    # path('logout/', logout, { 'template_name':'accouts/logout.html' }),

    path('register/', views.register , name='register'),

]