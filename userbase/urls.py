from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import MemberSignUpView, UserProfileView, PurchaseHistoryView, UserProductsView, OrderDetailView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', MemberSignUpView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('purchases/', PurchaseHistoryView.as_view(), name='purchase-history'),
    path('products/', UserProductsView.as_view(), name='user-products'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
]
