import pytest
from django.contrib.auth import get_user_model
from main.models import Category, Product


# Fixture for creating a user
@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='testpass123')


# Fixture for product data
@pytest.fixture
def product_data(db):
    category = Category.objects.create(name="Test Category", description="Test Description")
    return {
        'name': 'Test Product',
        'description': 'Test Description',
        'long_description': 'Detailed description here',
        'price': 9.99,
        'previous_price': 8.99,
        'stock': 100,
        'available': True,
        'categories': [category.id],  # Assuming your form handles category IDs for M2M relationships
    }


@pytest.fixture
def another_user(db):
    User = get_user_model()
    return User.objects.create_user(username='anotheruser', password='testpass123')


@pytest.fixture
def product(user, db):
    category = Category.objects.create(name="Electronics", description="Gadgets and more")
    product = Product.objects.create(
        name="Old Product",
        description="Old description",
        price=100.00,
        seller=user,
        stock=10,
        available=True
    )
    product.categories.add(category)  # Associate the category with the product
    return product
