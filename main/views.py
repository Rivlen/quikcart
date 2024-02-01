from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
from main.models import Product, Category


class HomePageView(View):
    def get(self, request):
        return render(request, 'index4.html')


class ProductListView(ListView):
    model = Product
    template_name = 'shop-list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop-single.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the features for the product
        context['features'] = self.object.features.all()
        # Additionally, add in a QuerySet of all the categories for the product
        context['categories'] = self.object.categories.all()
        return context
