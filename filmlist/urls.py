from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name="login"),
    path('home/', views.home, name="home"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('search/', views.search, name="search"),
    path('watch/<int:tmdb_id>/', views.watch_movie, name="watch"),
]
