from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import profile

app_name = "accounts"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]