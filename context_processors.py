from .models import Category, ProfileCategory, ProfileAuthor


def simple_book_store_processor(request):
    categories = Category.objects.all()

    values = {
        'categories': categories,
        'profile_categories': [],
        'profile_authors': []
    }

    if request.user.is_authenticated:
        profile_categories = ProfileCategory.objects.filter(profile=request.user.profile, status=1)
        profile_authors = ProfileAuthor.objects.filter(profile=request.user.profile, status=1)

        values["profile_categories"] = [v['category_id'] for v in profile_categories.values() if 'category_id' in v]
        values["profile_authors"] = [v['author_id'] for v in profile_authors.values() if 'author_id' in v]

    return values
