import pytest
from django.urls import reverse

from main.models import Product


# Test for successful product addition by an authenticated user
@pytest.mark.django_db
def test_product_add_view_success(client, user, product_data):
    client.force_login(user)
    url = reverse('product-add')
    response = client.post(url, product_data, follow=True)

    assert response.status_code == 200
    assert Product.objects.filter(name='Test Product').exists()

    # Verify the product is linked to the user
    product = Product.objects.get(name='Test Product')
    assert product.seller == user


# Test for redirecting unauthenticated user to login page
@pytest.mark.django_db
def test_product_add_view_unauthenticated(client, product_data):
    url = reverse('product-add')
    response = client.post(url, product_data)

    # Check if redirected to login
    assert response.status_code == 302
    login_url = reverse('login')  # Ensure this is the name of your login URL
    assert login_url in response.url


@pytest.mark.django_db
def test_product_update_view_success(client, user, product):
    client.force_login(user)
    url = reverse('product-update', kwargs={'pk': product.pk})
    updated_data = {
        'name': 'Updated Product',
        'description': 'Updated description',
        'price': 150.00,
        'stock': 10,
        'categories': [product.categories.first().pk],  # Assuming a M2M relation with categories
    }
    response = client.post(url, updated_data)
    product.refresh_from_db()

    assert response.status_code == 302  # Assuming redirection to 'home' on success
    assert product.name == 'Updated Product'
    assert product.description == 'Updated description'
    assert product.price == 150.00


@pytest.mark.django_db
def test_product_update_view_unauthorized(client, another_user, product):
    client.force_login(another_user)
    url = reverse('product-update', kwargs={'pk': product.pk})
    response = client.get(url)

    # Check for a 404 Not Found status code, indicating the product could not be accessed or found
    assert response.status_code == 404


@pytest.mark.django_db
def test_product_update_view_unauthenticated(client, product):
    url = reverse('product-update', kwargs={'pk': product.pk})
    response = client.get(url)

    assert response.status_code == 302
    assert reverse('login') in response.url


@pytest.mark.django_db
def test_product_delete_by_owner(client, user, product):
    client.login(username='testuser', password='testpass123')
    url = reverse('product-delete', kwargs={'pk': product.pk})
    response = client.post(url)
    assert response.status_code == 302
    assert not Product.objects.filter(pk=product.pk).exists()
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_product_delete_unauthorized(client, another_user, product):
    client.login(username='anotheruser', password='testpass123')
    url = reverse('product-delete', kwargs={'pk': product.pk})
    response = client.post(url)
    # Assuming your view redirects unauthorized attempts, check for redirect status code
    assert response.status_code == 404
    assert Product.objects.filter(pk=product.pk).exists()  # The product still exists


@pytest.mark.django_db
def test_product_delete_unauthenticated(client, product):
    url = reverse('product-delete', kwargs={'pk': product.pk})
    response = client.post(url)
    # Assuming your view redirects unauthenticated attempts, check for redirect status code
    assert response.status_code == 302
    assert reverse('login') in response.url  # Check redirection to login
    assert Product.objects.filter(pk=product.pk).exists()  # The product still exists
