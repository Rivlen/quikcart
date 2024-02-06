from django.urls import path
from main.views import HomePageView, ProductDetailView, CategoryListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('product-list/<int:pk>/', CategoryListView.as_view(), name='shop-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='shop-single'),
]
