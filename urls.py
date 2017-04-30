from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout_view, name="logout"),

    url(r'^book/(?P<pk>\d+)/$', views.BookView.as_view(), name='book'),
    url(r'^category/(?P<pk>\d+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^author/(?P<pk>\d+)/$', views.AuthorView.as_view(), name='author'),

    url(r'^user-books/(?P<status>\d+)/$', views.UserBooksView.as_view(), name='user-books'),

    url(r'^search/$', views.SearchView.as_view(), name='search'),

    url(r'^api/rate/$', views.rate_view, name='rate'),
    url(r'^api/follow/$', views.follow_view, name='follow'),
    url(r'^api/book-action/$', views.book_action_view, name='book-action'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
