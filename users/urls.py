
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from . import views


app_name = 'users'
urlpatterns = [
    #включить URL авторизацию по умолчанию
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    
    ]
