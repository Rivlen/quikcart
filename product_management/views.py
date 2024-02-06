from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from main.models import Product
from product_management.forms import ProductForm


class ProductAddView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product-add.html'
    success_url = reverse_lazy('shop-list', kwargs={'pk': 1})

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
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

    def dispatch(self, request, *args, **kwargs):
        """
        Overriding the dispatch method to add additional checks
        before proceeding with the GET or POST request.
        """
        obj = self.get_object()
        if obj.seller != self.request.user:
            raise PermissionDenied("You are not allowed to edit this product.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirects to the 'shop-list' of the current user's products after successful update.
        You might want to adjust this to redirect to the product detail view or any other view.
        """
        # Adjust the success_url as needed. This is just a placeholder.
        return reverse_lazy('shop-list', kwargs={'pk': self.object.categories.first().id})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'product-delete.html'

    def get_queryset(self):
        """
        Ensure that a user can only delete products they have listed.
        """
        qs = super().get_queryset()
        return qs.filter(seller=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        """
        Adds additional security to ensure that only the seller can request deletion.
        """
        obj = self.get_object()
        if obj.seller != self.request.user:
            raise PermissionDenied("You are not allowed to delete this product.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirects to the 'shop-list' of the current user's products after successful deletion.
        You might want to adjust this to redirect to a more appropriate view.
        """
        # Adjust the success_url as needed. This is just a placeholder.
        return reverse_lazy('shop-list', kwargs={'pk': 1})  # Or any other URL you see fit
