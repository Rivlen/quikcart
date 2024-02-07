from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from main.models import Product, Category


# class HomePageView(View):
#     def get(self, request):
#         return render(request, 'index4.html')


# beta homepage
class HomePageView(ListView):
    model = Product
    template_name = 'shop-list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        """
        Override the default context data to include the list of categories.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent__isnull=True)

        context['category_name'] = "Category"

        return context


class CategoryListView(ListView):
    model = Product
    template_name = 'shop-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Override the default queryset to return products from a specific category.
        """
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(Category, id=category_id)
        return Product.objects.filter(categories=category)

    def get_context_data(self, **kwargs):
        """
        Override the default context data to include the list of categories.
        """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context['categories'] = Category.objects.filter(parent_id=category_id)

        # Provide category name
        context['category_name'] = get_object_or_404(Category, id=category_id).name

        return context


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



