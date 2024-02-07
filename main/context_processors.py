from main.models import Category


def categories(request):
    # Fetch only parent categories (those without a parent)
    parent_categories = Category.objects.filter(parent__isnull=True)
    # Prepare a dictionary to hold categories and their subcategories
    categories_with_subcategories = {}
    for category in parent_categories:
        # Fetch subcategories for each parent category
        subcategories = Category.objects.filter(parent=category)
        categories_with_subcategories[category] = subcategories
    return {'categories_with_subcategories': categories_with_subcategories}

