from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from main.models import Product
from product_management.forms import ProductForm


class ProductAddView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product-add.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product-update.html'

    def get_queryset(self):
        """
        This method is an implicit object-level permission management.
        It ensures that a user can only update products they have listed.
        """
        qs = super().get_queryset()
        return qs.filter(seller=self.request.user)

    def get_success_url(self):
        """
        Redirects to the 'shop-list' of the current user's products after successful update.
        You might want to adjust this to redirect to the product detail view or any other view.
        """
        # Adjust the success_url as needed. This is just a placeholder.
        return reverse_lazy('home')

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        return obj.seller == user


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'product-delete.html'

    def get_queryset(self):
        """
        Ensure that a user can only delete products they have listed.
        """
        qs = super().get_queryset()
        return qs.filter(seller=self.request.user)

    def get_success_url(self):
        """
        Redirects to the 'shop-list' of the current user's products after successful deletion.
        You might want to adjust this to redirect to a more appropriate view.
        """
        # Adjust the success_url as needed. This is just a placeholder.
        return reverse_lazy('home')  # Or any other URL you see fit

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        return obj.seller == user
