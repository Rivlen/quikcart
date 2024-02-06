from django import forms
from main.models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'long_description', 'price', 'previous_price', 'stock', 'available',
                  'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
        }
