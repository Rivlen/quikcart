import pytest
from django.contrib.auth.models import Group
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_member_sign_up_success(client):
    # Ensure the "Member" group exists for the test
    Group.objects.get_or_create(name='Member')

    # The URL for your sign-up view
    url = reverse('register')

    # Mock valid form data
    form_data = {
        'username': 'testuser',
        'password1': 'strongpassword123',
        'password2': 'strongpassword123',  # Adjust field names based on your form
        # Add other required fields as necessary
    }

    response = client.post(url, form_data)

    # Check redirection to the 'login' page
    assertRedirects(response, reverse('login'))

    # Verify user creation
    User = get_user_model()
    assert User.objects.filter(username='testuser').exists()

    user = User.objects.get(username='testuser')
    assert user is not None

    # Verify group assignment
    assert user.groups.filter(name='Member').exists()


@pytest.mark.django_db
def test_member_sign_up_form_invalid(client):
    url = reverse('register')

    # Mock invalid form data (e.g., non-matching passwords)
    form_data = {
        'username': 'testuser',
        'password1': 'strongpassword123',
        'password2': 'wrongpassword',  # Deliberately incorrect
        # Add other fields if necessary
    }

    response = client.post(url, form_data)

    # Check the response does not redirect (stays on the form)
    assert response.status_code == 200
    assertTemplateUsed(response, 'register.html')

    User = get_user_model()
    # Verify no user is created
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username='testuser')


# Test that unauthenticated users are redirected to login
def test_user_profile_view_redirect_if_not_logged_in(client):
    url = reverse('user-profile')
    response = client.get(url)
    assert response.status_code == 302
    assert "/user/login/" in response.url  # Adjust this path based on your login URL configuration


# Test that authenticated users can access the profile view
def test_user_profile_view_for_logged_in_user(client, authenticated_user):
    url = reverse('user-profile')
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, 'user-profile.html')  # Ensure the correct template is used
    # Add more asserts here if you're adding additional context data to the view


@pytest.mark.django_db
def test_login_view_access(client):
    """Test that the login page can be accessed."""
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert 'login.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_login_success(client, user):
    """Test logging in with valid credentials redirects to the correct page."""
    url = reverse('login')
    response = client.post(url, {'username': 'testuser', 'password': 'testpass123'}, follow=True)
    assert response.context['user'].is_authenticated
    # Check the redirection path if there is a specific one, e.g., to the home page
    # assert response.redirect_chain[0][0] == reverse('home_page_name')


@pytest.mark.django_db
def test_login_failure(client, user):
    """Test logging in with invalid credentials does not redirect."""
    url = reverse('login')
    response = client.post(url, {'username': 'testuser', 'password': 'wrongpassword'})
    assert 'login.html' in (t.name for t in response.templates)
    assert not response.context['user'].is_authenticated


@pytest.mark.django_db
def test_purchase_history_view_access(client, user, order):
    client.login(username='testuser', password='testpass123')
    response = client.get(reverse('purchase-history'))
    assert response.status_code == 200
    assert 'purchase-history.html' in (t.name for t in response.templates)
    assert order in response.context['orders']


@pytest.mark.django_db
def test_user_products_view_access(client, user, product):
    client.login(username='testuser', password='testpass123')
    response = client.get(reverse('user-products'))
    assert response.status_code == 200
    assert 'user-products.html' in (t.name for t in response.templates)
    assert product in response.context['products']


@pytest.mark.django_db
def test_order_detail_view_for_owner(user, order):
    client = Client()
    client.force_login(user)
    url = reverse('order-detail', kwargs={'order_id': order.id})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_detail_view_for_another_user(another_user, order):
    client = Client()
    client.force_login(another_user)
    url = reverse('order-detail', kwargs={'order_id': order.id})
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_order_detail_view_for_unauthenticated_user(order):
    client = Client()
    url = reverse('order-detail', kwargs={'order_id': order.id})
    response = client.get(url)
    assert response.status_code == 302
    assert reverse('login') in response.url
