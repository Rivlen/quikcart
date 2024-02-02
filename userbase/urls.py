# userbase/urls.py
from django.urls import path
from .views import MemberSignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', MemberSignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
