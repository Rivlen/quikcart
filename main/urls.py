from django.urls import path
from main.views import HomePageView, ProductDetailView, ProductListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('product-list/<int:pk>/', ProductListView.as_view(), name='shop-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='shop-single'),
]
