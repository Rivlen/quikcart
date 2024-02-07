from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views import generic, View
from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy

from checkout.models import Order
from main.models import Product
from .forms import MemberRegistrationForm


class MemberSignUpView(generic.CreateView):
    form_class = MemberRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        members_group = Group.objects.get(name='Member')
        self.object.groups.add(members_group)
        return response

    def get_context_data(self, **kwargs):
        """
        Override the default context data to include the list of categories.
        """
        context = super().get_context_data(**kwargs)
        return context


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here if needed
        return context


class PurchaseHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'purchase-history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        """Filter orders to only those made by the current user."""
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class UserProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'user-products.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Filter products to only those listed by the current user."""
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')


class OrderDetailView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_items = order.items.all()
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'order-detail.html', context)
