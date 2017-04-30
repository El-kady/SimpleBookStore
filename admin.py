from django.contrib import admin
from .models import Category, Book, Author, Notification, ProfileCategory, ProfileAuthor, User, Profile
from django.db.models import Q


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    def save_model(self, request, book, form, change):
        super(BookAdmin, self).save_model(request, book, form, change)
        if change == False:
            category_profile_ids = ProfileCategory.objects.filter(category=book.category,status=1).values_list('profile_id', flat=True)
            author_profile_ids = ProfileAuthor.objects.filter(author=book.author,status=1).values_list('profile_id', flat=True)

            profiles = Profile.objects.filter(Q(id__in=category_profile_ids) | Q(id__in=author_profile_ids))

            for profile in profiles:
                obj, created = Notification.objects.update_or_create(
                    user=profile.user, book=book,
                    defaults={'read': False}
                )


admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
