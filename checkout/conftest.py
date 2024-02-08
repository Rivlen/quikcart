import pytest
from django.contrib.auth import get_user_model

from checkout.models import Order, Address, OrderItem
from main.models import Product, Category


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', password='password123')


@pytest.fixture
def product(db, user):
    category = Category.objects.create(name='Gadgets', description='Tech Gadgets')
    product = Product.objects.create(
        name='Phone',
        description='Smartphone',
        price=999.99,
        stock=10,
        available=True,
        seller=user
    )
    product.categories.add(category)  # Associate the category with the product
    return product


@pytest.fixture
def cart_with_product(client, product):
    session = client.session
    session['cart'] = {str(product.id): 1}
    session.save()


@pytest.fixture
def cart_with_multiple_products(client, product):
    # Assuming you have a product factory to create multiple products
    product1 = product
    product2 = product
    session = client.session
    session['cart'] = {str(product1.id): 1, str(product2.id): 2}  # Add two products to cart
    session.save()
    return product1, product2


@pytest.fixture
def another_product(db, user):
    category = Category.objects.create(name='Gadgets', description='Tech Gadgets')
    product = Product.objects.create(
        name='Samsung',
        description='Smartphone',
        price=999.99,
        stock=10,
        available=True,
        seller=user
    )
    product.categories.add(category)  # Associate the category with the product
    return product


@pytest.fixture
def address(db):
    return Address.objects.create(street="Main", street_number='12', city="Anytown", postal_code="12345", country="USA")


@pytest.fixture
def order(db, user, address):
    return Order.objects.create(user=user, address=address, name="John Doe", surname="Doe", email="john@example.com",
                                phone_number="1234567890", payment_method='CC', status=Order.PROCESSING)


@pytest.fixture
def order_item(db, order, product):
    return OrderItem.objects.create(order=order, product=product, quantity=2)
