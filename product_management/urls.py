from django.urls import path
from product_management.views import ProductAddView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    path('add/', ProductAddView.as_view(), name='product-add'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
]
