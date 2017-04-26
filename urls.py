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

    url(r'^api/rate/$', views.rate_view, name='rate'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
