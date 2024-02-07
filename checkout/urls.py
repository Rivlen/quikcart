from django.urls import path
from .views import CartView, AddToCartView, UpdateCartView, RemoveFromCartView, CheckoutView, OrderConfirmationView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('update/<int:product_id>/', UpdateCartView.as_view(), name='update-cart'),
    path('remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-success/<int:order_id>/', OrderConfirmationView.as_view(), name='order-success'),
]
