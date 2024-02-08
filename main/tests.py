import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_home_page_view(client, product, categories):
    url = reverse('home')
    response = client.get(url)

    # Check that the view returns a 200 status code
    assert response.status_code == 200

    # Check that the correct template is used
    assertTemplateUsed(response, 'shop-list.html')

    # Check that context contains 'products' and 'categories'
    assert 'products' in response.context
    assert len(response.context['products']) == 1  # Assuming only one product in the test DB
    assert 'categories' in response.context
    assert len(response.context['categories']) == 1  # Assuming only one category in the test DB
    assert response.context['category_name'] == "Category"


@pytest.mark.django_db
def test_product_list_view(client, product, categories):
    url = reverse('shop-list', kwargs={'pk': 1})
    response = client.get(url)

    # Check that the view returns a 200 status code
    assert response.status_code == 200

    # Check that the correct template is used
    assertTemplateUsed(response, 'shop-list.html')

    # Check that context contains 'products' and 'categories'
    assert 'products' in response.context
    assert len(response.context['products']) == 1  # Assuming only one product in the test DB
    assert 'categories' in response.context
    assert len(response.context['categories']) == 1  # Assuming only one category in the test DB
    assert response.context['category_name'] == categories[0].name  # Check that correct category name is used


@pytest.mark.django_db
def test_product_detail_view(client, product, categories):

    response = client.get(reverse('shop-single', kwargs={'pk': product.id}))

    assert response.status_code == 200
    assertTemplateUsed(response, 'shop-single.html')

    # Verify that the product detail is correctly displayed
    assert product.name in response.content.decode('utf-8')
    assert product.description in response.content.decode('utf-8')

    # Verify that the product's categories are included in the context and displayed
    categories_in_context = response.context['categories_with_subcategories']

    # Flatten the dictionary into a list of tuples (Parent, Child)
    flattened_list = [(parent, child) for parent, children in categories_in_context.items() for child in children]

    assert categories in flattened_list
    assert categories[0].name in response.content.decode('utf-8')
