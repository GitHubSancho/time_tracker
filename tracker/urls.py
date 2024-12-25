from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('home', views.home_view, name='home'),
    path('record-time/', views.record_time, name='record_time'),
    path('success/', views.success_view, name='success'),
]
