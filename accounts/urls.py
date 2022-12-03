from django.urls import path
from .views import login_view , logout_view , register
from mgapp import views
urlpatterns = [
    path('login-user' , login_view , name='login'),
    path('admin-dashboard', views.admindash , name='admin-dash'),
    path('logout' , logout_view , name='logout'),
    path('Sign-up', register , name='register')

]
