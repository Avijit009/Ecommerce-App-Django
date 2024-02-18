from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.sign_up, name='signup'),
    path('login/',views.log_in, name='login'),
    path('logout/',views.log_out, name='logout'),
    path('profile/',views.user_profile, name='profile'),
    path('vendor/', views.create_vendor, name='vendor'),
    path('password_change/', views.password_change, name='password_change')
]