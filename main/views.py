from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product


class HomePageView(View):
    def get(self, request):
        return render(request, 'index.html')


class ProductListView(ListView):
    model = Product
    template_name = 'shop-grid.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop-grid.html'
    context_object_name = 'product'
