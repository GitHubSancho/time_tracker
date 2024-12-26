from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    path('home', views.home_view, name='home'),
    path('home', views.dashboard_view, name='dashboard'),
    path('settings', views.settings_view, name='settings'),
    path('activity_log', views.activity_log_view, name='activity_log'),
    path('logout', views.logout_view, name='logout'),
    path('static_navigation',
         views.static_navigation_view,
         name='static_navigation'),
    path('password_reset', views.password_reset_view, name='password_reset'),
    path('password_reset', views.password_reset_view, name='password_reset'),
    path('a401', views.a401_view, name='a401'),
    path('a404', views.a404_view, name='a404'),
    path('a500', views.a500_view, name='a500'),
    path('charts', views.charts_view, name='charts'),
    path('tables', views.tables_view, name='tables'),
    path('light_sidenav', views.light_sidenav_view, name='light_sidenav'),
    path('record-time/', views.record_time, name='record_time'),
    path('success/', views.success_view, name='success'),
]
