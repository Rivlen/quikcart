import pytest
from django.contrib.auth import get_user_model
from main.models import Product, Category
from checkout.models import Order, OrderItem


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', email='test@example.com', password='testpass123')


# Fixture for authenticated user
@pytest.fixture
def authenticated_user(client, db):
    user_model = get_user_model()
    user = user_model.objects.create_user(username='user', password='testpass123')
    client.login(username='user', password='testpass123')
    return user


@pytest.fixture
def category(db):
    return Category.objects.create(name="Electronics", description="Electronic Items")


@pytest.fixture
def product(user, category, db):
    product = Product.objects.create(
        name='Test Product',
        seller=user,
        price=10.00,
        stock=5,
        available=True
    )
    product.categories.add(category)
    return product


@pytest.fixture
def order(user, product, db):
    order = Order.objects.create(user=user)
    OrderItem.objects.create(order=order, product=product, quantity=2)
    return order


@pytest.fixture
def another_user():
    User = get_user_model()
    return User.objects.create_user(username='anotheruser', password='12345')
