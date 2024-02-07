import pytest

from main.models import Category, Product
from userbase.models import User


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='12345')


@pytest.fixture
def categories():
    # Create a parent category and a child category for testing
    parent_category = Category.objects.create(name='Parent Category', description='A parent category')
    child_category = Category.objects.create(name='Child Category', description='A child category',
                                             parent=parent_category)
    return parent_category, child_category


@pytest.fixture
def product(user, categories):
    product = Product.objects.create(
        seller=user,
        name="Test Product",
        description="A product description",
        price=9.99,
        stock=100,
        available=True,
    )
    product.categories.add(categories[0])
    return product
