from django.views.generic import TemplateView
from .models import Order


class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            current_cart = Order.objects.get(user=self.request.user, status=Order.CART)
            cart_items = current_cart.items.all()
        except Order.DoesNotExist:
            cart_items = []
        context['cart_items'] = cart_items
        return context
