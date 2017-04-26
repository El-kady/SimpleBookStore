from .models import Category


def simple_book_store_processor(request):
    categories = Category.objects.all()
    return {
        'categories': categories
    }
