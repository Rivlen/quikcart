from main.models import Category


def categories(request):
    return {'categories_all': Category.objects.all()}
