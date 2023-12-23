from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name="app/login.html"), name="login"),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.update_item, name='update_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('about_us/', views.about_us, name='about_us'),
]