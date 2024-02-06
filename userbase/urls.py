from django.urls import path
from .views import MemberSignUpView, UserProfileView, PurchaseHistoryView, UserProductsView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', MemberSignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('purchases/', PurchaseHistoryView.as_view(), name='purchase-history'),
    path('products/', UserProductsView.as_view(), name='user-products'),
]
