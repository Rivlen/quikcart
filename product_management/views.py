from django.contrib.auth.mixins import LoginRequiredMixin
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


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product-update.html'  # Specify your template
    success_url = reverse_lazy('shop-list', kwargs={'pk': 1})  # Adjust to your named URL for listing products


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product-delete.html'  # Specify your template
    success_url = reverse_lazy('shop-list', kwargs={'pk': 1})  # Adjust to your named URL for the product list
